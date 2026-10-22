# 医院业务系统(Hospital Business System)

基于 Django + SQLite 的小型医院业务演示系统,含科室、医生、患者、挂号、就诊记录
五大模块,内置测试数据。

## 功能

- 科室管理(列表 + 新增)
- 医生管理(列表 + 新增,按科室归属)
- 患者管理(建档,含年龄自动计算)
- 挂号管理(挂号 + 完成/取消状态流转)
- 就诊记录(病历:主诉/诊断/处方,建病历自动把挂号置为「已就诊」)
- 总览仪表盘(各类计数 + 今日/待诊/已诊统计)
- Django 后台管理 `/admin/`

## 快速开始

```bash
cd /home/lihui/django_workspace/hospital_sys

# 首次:建表
../venv/bin/python manage.py migrate

# 写入测试数据(可重复执行,先清空再重建)
../venv/bin/python manage.py seed_data

# 启动(本机 8001 端口,避免与气象项目 8000 冲突)
../venv/bin/python manage.py runserver 0.0.0.0:8001
```

浏览器打开 http://127.0.0.1:8001/

后台管理:先 `../venv/bin/python manage.py createsuperuser`,再访问 `/admin/`。

## 数据模型

```
Department(科室) 1 ── * Doctor(医生)
Patient(患者)    1 ── * Registration(挂号)
Doctor           1 ── * Registration
Registration     1 ── 1 MedicalRecord(就诊记录)
```

## 测试数据(seed_data)

- 8 个科室:内科、外科、儿科、妇产科、骨科、眼科、口腔科、皮肤科
- 10 名医生(不同职称)
- 10 名患者
- 12 条挂号记录(含待就诊/已就诊/已取消三种状态)
- 8 条就诊记录(主诉/诊断/处方)
