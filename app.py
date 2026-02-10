from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import json

from config import Config
from database import db, Admin, Enquiry, Video, Statistic

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# Create necessary folders
folders = ['static/videos', 'static/images', 'static/gifs', 'static/uploads']
for folder in folders:
    os.makedirs(folder, exist_ok=True)

def allowed_file(filename, file_type='video'):
    if file_type == 'video':
        allowed = app.config['ALLOWED_VIDEO_EXTENSIONS']
    else:
        allowed = app.config['ALLOWED_IMAGE_EXTENSIONS']
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed

# ============================================
# MAIN WEBSITE ROUTES
# ============================================

@app.route('/')
def index():
    stats = Statistic.query.order_by(Statistic.display_order).all()
    featured_videos = Video.query.filter_by(is_featured=True).limit(3).all()
    return render_template('index.html', stats=stats, featured_videos=featured_videos)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/programs')
def programs():
    return render_template('programs.html')

@app.route('/methodology')
def methodology():
    return render_template('methodology.html')

@app.route('/outcomes')
def outcomes():
    return render_template('outcomes.html')

@app.route('/videos')
def videos_page():
    videos = Video.query.order_by(Video.upload_date.desc()).all()
    categories = db.session.query(Video.category).distinct().all()
    return render_template('videos.html', videos=videos, categories=categories)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        enquiry = Enquiry(
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form['phone'],
            college=request.form.get('college', ''),
            program=request.form.get('program', ''),
            message=request.form.get('message', '')
        )
        db.session.add(enquiry)
        db.session.commit()
        flash('Thank you for your enquiry! We will contact you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/api/statistics')
def get_statistics():
    stats = Statistic.query.order_by(Statistic.display_order).all()
    stats_data = [{
        'name': stat.name,
        'value': stat.value,
        'icon': stat.icon,
        'color': stat.color
    } for stat in stats]
    return jsonify(stats_data)

# ============================================
# ADMIN ROUTES - ADD THESE MISSING ROUTES
# ============================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        admin = Admin.query.filter_by(username=username, is_active=True).first()
        
        if admin and check_password_hash(admin.password, password):
            admin.last_login = datetime.utcnow()
            db.session.commit()
            login_user(admin)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('Logged out successfully', 'info')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    enquiries = Enquiry.query.order_by(Enquiry.created_at.desc()).all()
    videos = Video.query.order_by(Video.upload_date.desc()).all()
    
    stats = {
        'total_enquiries': Enquiry.query.count(),
        'new_enquiries': Enquiry.query.filter_by(status='New').count(),
        'total_videos': Video.query.count(),
        'featured_videos': Video.query.filter_by(is_featured=True).count(),
    }
    
    return render_template('admin/dashboard.html', 
                         enquiries=enquiries, 
                         videos=videos, 
                         stats=stats)

# ADD THESE CRITICAL MISSING ROUTES:
@app.route('/admin/enquiry/<int:id>/update', methods=['POST'])
@login_required
def update_enquiry_status(id):
    enquiry = Enquiry.query.get_or_404(id)
    enquiry.status = request.form['status']
    db.session.commit()
    flash('Enquiry status updated!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/enquiry/<int:id>/delete', methods=['POST'])
@login_required
def delete_enquiry(id):
    enquiry = Enquiry.query.get_or_404(id)
    db.session.delete(enquiry)
    db.session.commit()
    flash('Enquiry deleted!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/video/upload', methods=['POST'])
@login_required
def upload_video():
    if 'video' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('admin_dashboard'))
    
    file = request.files['video']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('admin_dashboard'))
    
    if file and allowed_file(file.filename, 'video'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        video = Video(
            title=request.form['title'],
            filename=filename,
            description=request.form.get('description', ''),
            category=request.form.get('category', 'Training'),
            is_featured='is_featured' in request.form
        )
        db.session.add(video)
        db.session.commit()
        
        flash('Video uploaded successfully!', 'success')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/video/<int:id>/delete', methods=['POST'])
@login_required
def delete_video(id):
    video = Video.query.get_or_404(id)
    
    # Delete file from server
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    
    db.session.delete(video)
    db.session.commit()
    flash('Video deleted!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/video/<int:id>/toggle-featured', methods=['POST'])
@login_required
def toggle_featured_video(id):
    video = Video.query.get_or_404(id)
    video.is_featured = not video.is_featured
    db.session.commit()
    status = "featured" if video.is_featured else "unfeatured"
    flash(f'Video {status} status updated!', 'success')
    return redirect(url_for('admin_dashboard'))

# ============================================
# FILE SERVING ROUTES
# ============================================

@app.route('/videos/<filename>')
def serve_video(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['IMAGE_UPLOAD_FOLDER'], filename)

@app.route('/gifs/<filename>')
def serve_gif(filename):
    return send_from_directory('static/gifs', filename)

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# ============================================
# INITIALIZATION
# ============================================

def initialize_database():
    with app.app_context():
        # Delete old database file to avoid conflicts
        db_file = 'metamorphosis.db'
        if os.path.exists(db_file):
            try:
                os.remove(db_file)
                print(f"🗑️  Removed old database file: {db_file}")
            except Exception as e:
                print(f"⚠️  Could not remove old database file: {e}")
        
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Create default admin if not exists
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(
                username='admin',
                password=generate_password_hash('admin123', method='sha256'),
                is_active=True
            )
            db.session.add(admin)
            print("👤 Default admin created: username='admin', password='admin123'")
        
        # Add default statistics
        if not Statistic.query.first():
            default_stats = [
                Statistic(name='Students Trained', value='5000+', icon='fa-user-graduate', color='#FF6B6B', display_order=1),
                Statistic(name='College Partners', value='50+', icon='fa-university', color='#4ECDC4', display_order=2),
                Statistic(name='Success Rate', value='95%', icon='fa-chart-line', color='#FFD166', display_order=3),
                Statistic(name='Program Modules', value='25+', icon='fa-layer-group', color='#06D6A0', display_order=4),
                Statistic(name='Workshop Hours', value='1000+', icon='fa-clock', color='#118AB2', display_order=5),
                Statistic(name='Cities Covered', value='15+', icon='fa-map-marker-alt', color='#EF476F', display_order=6),
            ]
            for stat in default_stats:
                db.session.add(stat)
            print("📊 Default statistics added")
        
        db.session.commit()
        print("✅ Database initialized successfully!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

