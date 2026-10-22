"""为医院业务系统写入演示测试数据。

用法: python manage.py seed_data
可重复执行:先清空再重建,保证数据确定。
"""
import datetime as dt
from django.core.management.base import BaseCommand
from django.utils import timezone

from hospital.models import (Department, Doctor, Patient, Registration, MedicalRecord)


class Command(BaseCommand):
    help = '写入医院业务系统的演示测试数据'

    def handle(self, *args, **opts):
        # 清空(先子后父,避免外键约束)
        MedicalRecord.objects.all().delete()
        Registration.objects.all().delete()
        Doctor.objects.all().delete()
        Patient.objects.all().delete()
        Department.objects.all().delete()

        # ---- 科室 ----
        deps = {}
        for name, desc in [
            ('内科', '呼吸、消化、心血管等常见内科疾病'),
            ('外科', '普外、创伤、骨科手术'),
            ('儿科', '0-14 岁儿童常见病'),
            ('妇产科', '妇科与产科'),
            ('骨科', '骨折、关节、脊柱'),
            ('眼科', '视力、眼底、青光眼'),
            ('口腔科', '牙体、牙周、正畸'),
            ('皮肤科', '湿疹、过敏、痤疮等皮肤病'),
        ]:
            deps[name] = Department.objects.create(name=name, description=desc)

        # ---- 医生 ----
        doctors = []
        doctor_specs = [
            ('内科', '陈志远', '主任医师', '心血管疾病'),
            ('内科', '刘敏', '主治医师', '呼吸系统疾病'),
            ('外科', '王建国', '副主任医师', '普外科手术'),
            ('外科', '张伟', '住院医师', '创伤急救'),
            ('儿科', '李晓红', '副主任医师', '儿童呼吸道感染'),
            ('妇产科', '赵丽华', '主任医师', '妇科肿瘤'),
            ('骨科', '孙国栋', '主治医师', '关节置换'),
            ('眼科', '周明', '副主任医师', '白内障手术'),
            ('口腔科', '吴倩', '主治医师', '牙体牙髓'),
            ('皮肤科', '郑洁', '住院医师', '过敏性疾病'),
        ]
        for dep_name, name, title, spec in doctor_specs:
            doctors.append(Doctor.objects.create(
                name=name, title=title, department=deps[dep_name], specialty=spec))

        # ---- 患者 ----
        patients = []
        patient_rows = [
            ('张大爷', '男', '1954-03-12', '13800001111', '北京市朝阳区'),
            ('李阿姨', '女', '1962-07-28', '13800002222', '北京市海淀区'),
            ('王小刚', '男', '1988-11-05', '13900003333', '北京市丰台区'),
            ('赵晓梅', '女', '1995-02-14', '13700004444', '北京市西城区'),
            ('刘子轩', '男', '2015-09-30', '13600005555', '北京市东城区'),
            ('陈雨桐', '女', '2018-06-21', '13500006666', '北京市通州区'),
            ('孙建国', '男', '1970-01-19', '13400007777', '北京市大兴区'),
            ('周婷婷', '女', '1992-08-08', '13300008888', '北京市昌平区'),
            ('吴海涛', '男', '1985-12-02', '13200009999', '北京市石景山区'),
            ('郑雅文', '女', '2001-04-25', '13100001010', '北京市门头沟区'),
        ]
        for name, gender, birth, phone, addr in patient_rows:
            patients.append(Patient.objects.create(
                name=name, gender=gender, birth_date=birth, phone=phone, address=addr))

        # ---- 挂号 + 就诊记录 ----
        today = timezone.localdate()
        def _d(days_ago):
            return today - dt.timedelta(days=days_ago)

        # (患者索引, 科室名, 医生名, 距今天数, 状态, 挂号费)
        reg_specs = [
            (0, '内科', '陈志远', 0, 'waiting', '15.00'),
            (1, '内科', '刘敏', 0, 'waiting', '10.00'),
            (2, '外科', '王建国', 0, 'done', '20.00'),
            (3, '妇产科', '赵丽华', 0, 'done', '20.00'),
            (4, '儿科', '李晓红', 1, 'done', '15.00'),
            (5, '儿科', '李晓红', 1, 'cancelled', '15.00'),
            (6, '骨科', '孙国栋', 1, 'done', '20.00'),
            (7, '眼科', '周明', 2, 'done', '15.00'),
            (8, '口腔科', '吴倩', 2, 'done', '10.00'),
            (9, '皮肤科', '郑洁', 3, 'done', '10.00'),
            (2, '外科', '张伟', 3, 'cancelled', '15.00'),
            (1, '内科', '陈志远', 4, 'done', '15.00'),
        ]
        # (挂号索引, 主诉, 诊断, 处方)
        record_specs = {
            2: ('右下腹疼痛 1 天', '急性阑尾炎', '建议住院手术,术前禁食水 8 小时'),
            3: ('停经 40 天,恶心', '早孕', '叶酸 0.4mg 每日 1 次;预约 B 超'),
            4: ('发热咳嗽 3 天', '急性支气管炎', '阿莫西林 0.25g 每日 3 次;多饮水休息'),
            6: ('左膝关节疼痛半年', '膝关节骨性关节炎', '布洛芬缓释 0.3g 每日 2 次;避免剧烈运动'),
            7: ('视物模糊 1 年', '老年性白内障', '建议择期行白内障超声乳化术'),
            8: ('牙痛 3 天', '急性牙髓炎', '开髓引流;阿莫西林 0.5g 每日 3 次'),
            9: ('面部皮疹伴瘙痒', '过敏性皮炎', '氯雷他定 10mg 每日 1 次;外涂炉甘石洗剂'),
            11: ('头晕胸闷', '高血压', '苯磺酸氨氯地平 5mg 每日 1 次;低盐饮食'),
        }

        regs = []
        for pi, dep_name, doc_name, days_ago, status, fee in reg_specs:
            doctor = next(d for d in doctors if d.name == doc_name)
            reg = Registration.objects.create(
                patient=patients[pi], department=deps[dep_name], doctor=doctor,
                visit_date=_d(days_ago), status=status, fee=fee)
            regs.append(reg)

        for reg_idx, (complaint, diag, rx) in record_specs.items():
            MedicalRecord.objects.create(
                registration=regs[reg_idx], chief_complaint=complaint,
                diagnosis=diag, prescription=rx)

        self.stdout.write(self.style.SUCCESS(
            f'测试数据写入完成:科室 {len(deps)}、医生 {len(doctors)}、'
            f'患者 {len(patients)}、挂号 {len(regs)}、就诊记录 {len(record_specs)}'))
