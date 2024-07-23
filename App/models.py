from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Campo1(models.TextChoices):
    SIM = 'S'
    NAO = 'N'
    
class Status(models.TextChoices):
    CADASTRADO = 'C', 'Cadastrado'
    EMTESTE = 'ET', 'Em Teste'
    TESTADO = 'T', 'Testado'
    RETESTADO = 'RE', 'Retestado'
    CAMPO = 'CP', 'Campo'

class EquipamentoRegistrado(models.Model):
    modelo = models.CharField(max_length=100)
    equipamento = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    problema = models.CharField(max_length=200)
    mac = models.CharField(max_length=17, unique=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.CADASTRADO)
    data_teste = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.equipamento} - {self.fabricante} - {self.problema} - {self.mac} - {self.status} - {self.data_teste} - {self.modelo}"

class EquipamentoEmTeste(models.Model):
    modelo = models.CharField(max_length=100)
    equipamento = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    problema = models.CharField(max_length=200)
    mac = models.CharField(max_length=17, unique=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.EMTESTE)
    data_teste = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.modelo} - {self.equipamento} - {self.fabricante} - {self.problema} - {self.mac} - {self.status} - {self.data_teste}"

class EquipamentoTestado(models.Model):
    modelo = models.CharField(max_length=100)
    equipamento = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    problema = models.CharField(max_length=200)
    relato_teste = models.CharField(max_length=800)
    mac = models.CharField(max_length=30, unique=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.TESTADO)
    data_teste = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    campo = models.CharField(max_length=1, choices=Campo1.choices)


    def __str__(self):
        return f"{self.modelo} - {self.equipamento} - {self.fabricante} - {self.problema} - {self.mac} - {self.relato_teste} - {self.status} - {self.data_teste} - {self.modelo}"

class EquipamentoReteste(models.Model):
    modelo = models.CharField(max_length=100)
    equipamento = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    problema = models.CharField(max_length=200)
    relato_teste = models.CharField(max_length=800)
    mac = models.CharField(max_length=30, unique=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.TESTADO)
    data_teste = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.modelo} - {self.equipamento} - {self.fabricante} - {self.problema} - {self.mac} - {self.relato_teste} - {self.status} - {self.data_teste}"
    
class EquipamentoRetestado(models.Model):
    modelo = models.CharField(max_length=100)
    equipamento = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    problema = models.CharField(max_length=200)
    relato_teste = models.CharField(max_length=800)
    mac = models.CharField(max_length=30, unique=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.TESTADO)
    data_teste = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.modelo} - {self.equipamento} - {self.fabricante} - {self.problema} - {self.mac} - {self.relato_teste} - {self.status} - {self.data_teste}"

class EquipamentoParaCampo(models.Model):
    modelo = models.CharField(max_length=100)
    equipamento = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    problema = models.CharField(max_length=200)
    relato_teste = models.CharField(max_length=800)
    mac = models.CharField(max_length=30, unique=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.CAMPO)
    data_teste = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.modelo} - {self.equipamento} - {self.fabricante} - {self.problema} - {self.mac} - {self.relato_teste} - {self.status} - {self.data_teste}"

class CadastroViabilidade(models.Model):
    projeto_responsavel = models.CharField(max_length=100)
    comercial_responsavel = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    descricao_projeto = models.TextField()
    descricao_comercial = models.TextField()
    coluna_timestamp = models.DateField(auto_now=True)
    

    def __str__(self):
        return f"{self.projeto_responsavel} - {self.comercial_responsavel} - {self.status} - {self.descricao_projeto} - {self.descricao_comercial} - {self.coluna_timestamp}"
    

class CadastroTecnicos(models.Model):
    projeto_responsavel = models.CharField(max_length=100)
    tecnico_responsavel = models.CharField(max_length=100)
    assunto = models.CharField(max_length=100)
    info_atendimento = models.TextField()
    date = models.DateField(auto_now=True)
    
    def __str__(self):
        return f"{self.projeto_responsavel} - {self.tecnico_responsavel} - {self.info_atendimento} - {self.assunto} - {self.date}"
    

class Tecnicos(models.Model):
    projeto_responsavel = models.CharField(max_length=100)
    tecnico_responsavel = models.CharField(max_length=100)
    info_atendimento = models.TextField()
    date = models.DateField(auto_now=True)
    hora = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.projeto_responsavel} - {self.tecnico_responsavel} - {self.info_atendimento} - {self.date} - {self.hora}"
        
