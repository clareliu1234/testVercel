from app import app, db
from models import User, Class_time_table


with app.app_context():
    # db.drop_all()
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='1873289781@qq.com', phone='17872001937', password='admin_password')
        admin.set_password('admin_password')  # 你应该选择一个更安全的密码

        db.session.add(admin)
        db.session.commit()

    class_time_table1 = Class_time_table(class_time='2024-6-25', class_title='家中家具摆放？其中学问很大',
                                         class_teacher='test1', class_content='家中家具到底怎么拜访呢？')

    db.session.add(class_time_table1)
    db.session.commit()
