# -*- coding: utf-8 -*-
import json

class Sight:
    level = 0
    zoom = 0

    def __init__(self,title,municipality,agr_rating):
        self.title = title
        self.municipality = municipality
        self.agr_rating = agr_rating
    
    def __str__(self):
        return f'Sight: title={self.title}, agr_rating={self.agr_rating}, lat={self.municipality.lat}, lng={self.municipality.lng}'

    def to_dict(self):
        return {
            'title': self.title,
            'lng': self.municipality.lng,
            'lat': self.municipality.lat,
            'zoom': self.zoom,
            'agr_rating': self.agr_rating,
            'level': self.level,
            'slices': self.get_slices(),
            'datatable': self.get_datatable()
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())
    
    def get_slices(self):
        pass

    def get_datatable(self):
        pass

class MunicipalitySight(Sight):
    level = 1
    zoom = 14

    def get_slices(self):
        return [ 
            { 'color': get_color_for_rating(self.agr_rating)} 
        ]

    def get_datatable(self):
        return [
            ['Категории', 'Актуальность'],
            ['Рейтинг',self.agr_rating]
        ]

class ConcreteSight(Sight):
    level = 2
    zoom = 20

    def get_slices(self):
        return [{'color': get_color_for_rating(self.agr_rating)} for qc in quality_characteristics]
        

    def get_datatable(self):
        result = [['Категория', 'Значение']]
        for qc in quality_characteristics:
            result.append([qc,self.agr_rating])
        return result

# есть ощущение, что на фронте координаты перепутаны
class Municipality:
    def __init__(self,name,lat,lng):
        self.name = name
        self.lat = lat
        self.lng = lng

KRASNODAR_GEOPOINT  = Municipality(name='Краснодар',lat=45.035760693570964,lng=38.97823870980312)
ABRAU_GEOPOINT      = Municipality(name='Абрау-Дюрсо',lat=44.68793782617598,lng=37.519190010583664)
ANAPA_GEOPOINT      = Municipality(name='Анапа',lat=44.89334960303149,lng=37.313022963754904)
GELENDZHIK_GEOPOINT = Municipality(name='Геленджик',lat=44.558945452551974,lng=38.06959051220287)
SOCHI_GEOPOINT      = Municipality(name='Сочи',lat=43.60358075905748,lng=39.73491323835603)
municipalities = (KRASNODAR_GEOPOINT,ANAPA_GEOPOINT,GELENDZHIK_GEOPOINT,ABRAU_GEOPOINT,SOCHI_GEOPOINT)

quality_characteristics = ("грязь на пляже",
					"пробки на дороге к морю",
					"высокие цены",
					"качество сервиса",
					"джиппинг",
					"экология",
					"скопления людей",
					"благоустройство")

def get_municipality_by_name(name):
    for mun in municipalities:
        if mun.name.lower() == name.lower():
            return mun

def get_color_for_rating(rating):
    if rating > 80:
        return 'green'
    if rating > 60:
        return 'yellow'
    if rating > 40:
        return 'orange'
    if rating > 20:
        return 'red'
    return 'blue'
