# -*- coding: utf-8 -*-
import spacy
import json

import dictionaries as d
import models as m
# TODO: заменить Ё на Е

# Загрузка русской NLP-модели
nlp = spacy.load('ru_core_news_md')

# основная функция - возвращает json
def get_json_with_parsed_reviews_info(reviews):
    result_list = parse_list_of_reviews(reviews)
    return json.dumps({
        'object_tour': [r.to_dict() for r in result_list]
    })

# обработка списка отзывов
def parse_list_of_reviews(reviews):
    concrete_sights, municipality_sights = [],[]
    mun_obj_type_combinations = []
    # Парсинг конкретных достопримечательностей
    for r in reviews:
        s = parse_a_review(r)
        # используем mun_obj_type_combinations для избавления от дубликатов (в разрезе города и вида достопримечательности)
        if s is not None:
            s_tuple = (s.title,s.municipality.name)
            if s_tuple not in mun_obj_type_combinations:
                concrete_sights.append(s)
                mun_obj_type_combinations.append(s_tuple)

    # Составление статистики для достопримечательностей-муниципалитетов
    for mun in m.municipalities:
        mun_score = 0.0
        mun_rating = 0.0
        total_sights = 0
        # рассчёт среднего рейтинга для каждого муниципалитета
        for cs in concrete_sights:
            if cs.municipality.name == mun.name:
                mun_score += cs.agr_rating
                total_sights += 1
        
        if total_sights > 0:
            mun_rating = round(mun_score / total_sights,2)
            mun_sight = m.MunicipalitySight(title=mun.name,municipality=mun,agr_rating=mun_rating)
            municipality_sights.append(mun_sight)
    
    return concrete_sights + municipality_sights
    
# обработка одного отзыва
def parse_a_review(text):
    # Парсинг текста с помощью spaCy
    doc = nlp(text)
    # на всякий случай приводим элементы словарей к леммам
    obj_lemmas = {get_lemma(w) for w in d.obj_types}

    # 1. выделение типов объектов
    doc_noun_lemmas = {token.lemma_ for token in doc if token.tag_ == 'NOUN' and not token.is_stop}
    doc_obj_types = doc_noun_lemmas.intersection(obj_lemmas)
    
    # 2. выделение географических мест
    mun_name_lemmas = {mun.name.lower() for mun in m.municipalities}
    doc_mun_lemmas = {entity.lemma_ for entity in doc.ents if entity.label_ == 'LOC' and entity.lemma_ in mun_name_lemmas}

    # 3. Выделение эмоциональных оценок (по заданному множеству)
    doc_noun_lemmas = {token.lemma_ for token in doc if token.is_alpha and not token.is_stop}
    doc_impressions = doc_noun_lemmas.intersection(set(d.impressions))

    # 4. Рассчёт среднего рейтинга для данной записи
    rating = 0.0
    if len(doc_impressions) > 0:
        total_score = 0
        for imp in doc_impressions:
            imp_score = d.impressions[imp]
            if imp_score is not None:
                total_score += imp_score

        rating = round(total_score / len(doc_impressions),2) * d.SCORE_MULTIPLICATOR
    
    # Если не хватает данных, пропускаем текст и возвращаем None
    if len(doc_mun_lemmas) == 0 or len(doc_obj_types) == 0:
        return None
    
    municipality = m.get_municipality_by_name(list(doc_mun_lemmas)[0])
    sight_title = list(doc_obj_types)[0].capitalize()
    return m.ConcreteSight(sight_title,municipality,rating)
    
# рассчёт леммы для слова
def get_lemma(word):
    word_doc = nlp(word)
    if len(word) > 1:
        return word
    token = word_doc[0]
    return token.lemma_
