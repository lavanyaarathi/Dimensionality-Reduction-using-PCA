from flask import Blueprint, render_template, request, redirect, url_for, flash
from modules.preprocessing import PreprocessingModule
from modules.upload_handler import FileUploadHandler
from modules.session_manager import session_manager
from config import Config
import os
from werkzeug.utils import secure_filename

preprocess_bp = Blueprint('preprocess', __name__, url_prefix='/preprocess')
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

@preprocess_bp.route('/', methods=['GET', 'POST'])
def preprocess():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            flash("No file selected.")
            return redirect(request.url)

        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)

        processor = PreprocessingModule()
        try:
            result = processor.process_file(filepath)
            if result["type"] == "tabular":
                return render_template('preprocess.html', 
                                       table_original=result["original_head"], 
                                       table_normalized=result["normalized_head"])
            else:
                result["resized"].save(os.path.join(Config.UPLOAD_FOLDER, "resized_" + filename))
                return render_template('preprocess.html', 
                                       image_path=url_for('static', filename="../" + filepath),
                                       shape=result["shape"])
        except Exception as e:
            flash(str(e))
            return redirect(request.url)
    return render_template('preprocess.html')
