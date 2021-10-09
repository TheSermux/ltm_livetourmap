# -*- coding: utf-8 -*-
import tour_score_parser as tsp
import analyzed_messages as am

# вызов функции, которая возвращает json
result = tsp.get_json_with_parsed_reviews_info(am.reviews_to_analyze)
print(result)
