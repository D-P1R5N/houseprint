from flask import render_template, url_for, flash, redirect, request, jsonify, Blueprint
from houseprint import app, db, bcrypt
from houseprint.users.models import User
from houseprint.inventory.models import Item, Inventory, Category
from flask_login import current_user, login_required
#Error Handlers
from sqlalchemy.exc import IntegrityError
import traceback


inv= Blueprint('inventory', __name__)

#@inv.before_request
#def print_ip():
#    print(request.__dict__)
#    print(request.remote_addr)
#    print(request.environ.get('REMOTE_ADDR', 'ADDR_NOT_FOUND'))

@inv.route("/inventory", methods=["GET", "POST", "PUT"])

def inventory():
    if not current_user.is_authenticated:
        return redirect(url_for('main.home'))
    category = Category.query.all()
    if request.method == 'POST':
        param = request.form.get('search', None)
        if param:
            inventory = Inventory.query.join(Item).filter_by(name=param).paginate(
                page=1, per_page=25)
            title = f"Inventory ~ {param}"
        else:
            return redirect(url_for("inventory.inventory"))

    elif request.method == 'GET':
        #We will pass a list of objects to Jinja. HTML is configured for the objects.
        page = request.args.get('page', 1, type=int)
        inventory = Inventory.query.join(Item).order_by(Item.name.desc())\
            .paginate(page=page, per_page=25)
        title = "Inventory"
        #inventory is a Pagination Object; use .pages & .items
    return render_template("inventory.html", _title=title,
        inventory=inventory.items, pages=inventory.pages, categories=category)

@inv.route("/inventory/_category", methods=["POST","PUT"])
def _category():
    category = request.json['category']
    _c = Category(name=category)
    try:
        db.session.add(_c)
        db.session.commit()
    except IntegrityError:
        db.rollback()
        flash(f'Unique Contraint Error, try renaming {category}')
        return "false"
    except Exception:
        flash(traceback.print_exc())
        return "false"
    finally:
        return category

@inv.route("/inventory/_barcode", methods=["POST","PUT"])
def _barcode():
    barcode = request.json['barcode']
    item = Item.query.filter_by(barcode=barcode).first()
    if item:
        return jsonify(item.payload())
    else:
        return "false"
