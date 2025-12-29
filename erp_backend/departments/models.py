from django.db import models

class SubDepartment(models.Model):
    name = models.CharField(max_length=120)
    department = models.ForeignKey('accounts.Department', on_delete=models.CASCADE, related_name="sub_departments")

    def __str__(self):
        return f"{self.department.name} → {self.name}"
