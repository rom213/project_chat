from flask import Blueprint, render_template

vehicles_bp = Blueprint('vehicles', __name__)

@vehicles_bp.route('')
def vehicles():
    return render_template('dashboard/body/body.html')

