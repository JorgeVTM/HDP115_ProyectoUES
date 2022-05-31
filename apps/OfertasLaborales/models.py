from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from os import system
# Create your models here.

#Modelo usuario persona
class Persona(models.Model):
    
    #Relación uno a uno con el modelo User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    #Propiedades de la tabla
    fecha_nacimiento = models.DateField(auto_now=False, auto_now_add=False, default=None, null=True)
    genero = models.CharField(max_length=50, default=None, null=True)
    edad = models.IntegerField(default=None, null=True)
    telefono = models.CharField(max_length=80, default=None, null=True)
    dui = models.CharField(max_length=80, default=None, null=True)
    direccion = models.CharField(max_length=200, default=None, null=True)
    
    #Metodo mostrar
    def __str__(self):
        texto = "nombre de usuario: {0}, primer nombre: {1}, edad: {2}"
        return texto.format(self.user.username, self.user.first_name, self.edad)
    
#Modelo para perfil laboral
class Perfil(models.Model):
    
    #Relación uno a uno con el modelo User
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    
    #Propiedades de la tabla
    formacion_academica = models.CharField(max_length=500, default=None, null=True)
    experiencia_laboral = models.CharField(max_length=500, default=None, null=True)
    cursos_realizados = models.CharField(max_length=500, default=None, null=True)
    idiomas = models.CharField(max_length=500, default=None, null=True)
    conocimientos_adicionales = models.CharField(max_length=500, default=None, null=True)
    
    #Metodo mostrar
    def __str__(self):
        user = User.objects.get(id=self.persona.user_id)
        texto = "nombre usuario: {0}, detalles: {1}"
        return texto.format(user.username, self.formacion_academica)

#Modelos de para las almacenar las ofertas laborales por categoria
class Categoria(models.Model):
    
    #Propiedades de la tabla
    nombre = models.CharField(max_length=100, default=None)

    def get_nombre(self):
        return self.nombre
    
    #Metodo mostrar
    def __str__(self):
        texto = "nombre: {0}"
        return texto.format(self.get_nombre())

#Modelos de para las almacenar las ofertas laborales por facultad
class Facultad(models.Model):
    
    #Propiedades de la tabla
    nombre = models.CharField(max_length=100, default=None)

    def get_nombre(self):
        return self.nombre
    
    #Metodo mostrar
    def __str__(self):
        texto = "nombre: {0}"
        return texto.format(self.get_nombre())

#Modelos de para las almacenar las ofertas laborales por sede
class Sede(models.Model):
    
    #Propiedades de la tabla
    nombre = models.CharField(max_length=100, default=None)
    ciudad = models.CharField(max_length=100, default=None, null=True)
    departamento = models.CharField(max_length=100, default=None, null=True)
    
    #Metodo mostrar
    def __str__(self):
        
        texto = "sede: {0}, departamento: {1}, ciudad: {2}"
        return texto.format(self.nombre, self.departamento, self.ciudad)

#Modelo para las ofertas laborales
class OfertaLaboral(models.Model):
    
    #Propiedades de la tabla
    area_de_trabajo = models.CharField(max_length=150, default=None, null=True)
    cargo_solicitado = models.CharField(max_length=150, default=None, null=True) 
    vacantes = models.CharField(max_length=150, default=None, null=True)
    tipo_contratacion = models.CharField(max_length=150, default=None, null=True)
    nivel_experiencia = models.CharField(max_length=150, default=None, null=True)
    generos = models.CharField(max_length=150, default=None, null=True)
    edad_solicitada = models.CharField(max_length=150, default=None, null=True)
    salario_minimo = models.DecimalField(max_digits=10000,decimal_places=2,default=0.00, null=True)
    salario_maximo = models.DecimalField(max_digits=10000,decimal_places=2,default=0.00, null=True)
    descripcion = models.CharField(max_length=1000, default=None, null=True)
    
    #Relaciones con los modelos
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    
    def __str__(self):  
        texto = 'Ofertas Laboral. area: {0}. cargo: {1}. vacante: {2}. salario: {3}.'    
        return texto.format(self.area_de_trabajo,self.cargo_solicitado,self.vacantes,self.salario_minimo)
    
#Modelo para las solicitudes laborales
class SolicitudLaboral(models.Model):

    #Relaciones con los modelos
    ofertalaboral = models.ForeignKey(OfertaLaboral, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        texto = 'oferta laboral: {0}. persona: {1}.'        
        return texto.format(self.ofertalaboral.area_de_trabajo,self.user.first_name)