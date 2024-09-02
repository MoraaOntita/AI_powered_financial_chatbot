from flask import Blueprint, render_template, request
from app.services.chatbot import get_answer

index_bp = Blueprint('index', __name__)

@index_bp.route('/', methods=['GET', 'POST'])
def index():
    answer = ""
    if request.method == 'POST':
        question = request.form.get('question')
        answer = get_answer(question)
    return render_template('index.html', answer=answer)
