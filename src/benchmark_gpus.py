from time import time

from ml_cloud_connector.MlCloudConnector import MlCloudConnector
from ollama import Client
from tqdm import tqdm

from configuration import TRANSLATIONS_PORT

# 550 characters
text_1 = """‫ﺍﻟﺷﻌﺏ‬‫ﺍﻟﺟﺯﺍﺋﺭﻱ‬ ‫ﺷﻌﺏ‬ ‫ﺣﺭ‪،‬‬ ‫ﻭﻣﺻﻣﻡ‬ ‫ﻋﻠﻰ‬ ‫ﺍﻟﺑﻘﺎء‬ ‫ﺣﺭﺍ‬ ‫‪.‬‬
‫ﻓﺗﺎﺭﻳﺧﻪ‬‫ﺍﻟﻁﻭﻳﻝ‬ ‫ﺳﻠﺳﻠﺔ‬ ‫ﻣﺗﺻﻠﺔ‬ ‫ﺍﻟﺣﻠﻘﺎﺕ‬ ‫ﻣﻥ‬ ‫ﺍﻟﻛﻔﺎﺡ‬ ‫ﻭﺍﻟﺟﻬﺎﺩ‪،‬‬ ‫ﺟﻌﻠﺕ‬ ‫ﺍﻟﺟﺯﺍﺋﺭ‬ ‫ﺩﺍﺋﻣﺎ‬ ‫ﻣﻧﺑﺕ‬ ‫ﺍﻟﺣﺭﻳﺔ‪،‬‬ ‫ﻭﺃﺭﺽ‬
‫ﺍﻟﻌﺯﺓ‬‫ﻭﺍﻟﻛﺭﺍﻣﺔ‬ ‫‪.‬‬
‫ﻟﻘﺩ‬‫ﻋﺭﻓﺕ‬ ‫ﺍﻟﺟﺯﺍﺋﺭ‬ ‫ﻓﻲ‬ ‫ﺃﻋﺯ‬ ‫ﺍﻟﻠﺣﻅﺎﺕ‬ ‫ﺍﻟﺣﺎﺳﻣﺔ‬ ‫ﺍﻟﺗﻲ‬ ‫ﻋﺎﺷﻬﺎ‬ ‫ﺍﻟﺑﺣﺭ‬ ‫ﺍﻷﺑﻳﺽ‬ ‫ﺍﻟﻣﺗﻭﺳﻁ‪،‬‬ ‫ﻛﻳﻑ‬ ‫ﺗﺟﺩ‬ ‫ﻓﻲ‬ ‫ﺃﺑﻧﺎﺋﻬﺎ‪،‬‬ ‫ﻣﻧﺫ‬
‫ﺍﻟﻌﻬﺩ‬‫ﺍﻟﻧﻭﻣﻳﺩﻱ‪،‬‬ ‫ﻭﺍﻟﻔﺗﺢ‬ ‫ﺍﻹﺳﻼﻣﻲ‪،‬‬ ‫ﺣﺗﻰ‬ ‫ﺍﻟﺣﺭﻭﺏ‬ ‫ﺍﻟﺗﺣﺭﻳﺭﻳﺔ‬ ‫ﻣﻥ‬ ‫ﺍﻻﺳﺗﻌﻣﺎﺭ‪،‬‬ ‫ﺭﻭﺍﺩﺍ‬ ‫ﻟﻠﺣﺭﻳﺔ‪،‬‬ ‫ﻭﺍﻟﻭﺣﺩﺓ‬ ‫ﻭﺍﻟﺭﻗﻲ‪،‬‬
‫ﻭﺑﻧﺎﺓ‬‫ﺩﻭﻝ‬ ‫ﺩﻳﻣﻘﺭﺍﻁﻳﺔ‬ ‫ﻣﺯﺩﻫﺭﺓ‪،‬‬ ‫ﻁﻭﺍﻝ‬ ‫ﻓﺗﺭﺍﺕ‬ ‫ﺍﻟﻣﺟﺩ‬ ‫ﻭﺍﻟﺳﻼﻡ‬ ‫‪.‬‬"""


# 1413 characters
text_2 = """‫ﻭﻛﺎﻥ‬‫ﺃﻭﻝ‬ ‫ﻧﻭﻓﻣﺑﺭ‬ ‫‪1954‬‬ ‫ﻧﻘﻁﺔ‬ ‫ﺗﺣﻭﻝ‬ ‫ﻓﺎﺻﻠﺔ‬ ‫ﻓﻲ‬ ‫ﺗﻘﺭﻳﺭ‬ ‫ﻣﺻﻳﺭﻫﺎ‬ ‫ﻭﺗﺗﻭﻳﺟﺎ‬ ‫ﻋﻅﻳﻣﺎ‬ ‫ﻟﻣﻘﺎﻭﻣﺔ‬ ‫ﺿﺭﻭﺱ‪،‬‬
‫ﻭﺍﺟﻬﺕ‬‫ﺑﻬﺎ‬ ‫ﻣﺧﺗﻠﻑ‬ ‫ﺍﻻﻋﺗﺩﺍءﺍﺕ‬ ‫ﻋﻠﻰ‬ ‫ﺛﻘﺎﻓﺗﻬﺎ‪،‬‬ ‫ﻭﻗﻳﻣﻬﺎ‪،‬‬ ‫ﻭﺍﻟﻣﻛﻭﻧﺎﺕ‬ ‫ﺍﻷﺳﺎﺳﻳﺔ‬ ‫ﻟﻬﻭﻳﺗﻬﺎ‪،‬‬ ‫ﻭﻫﻲ‬ ‫ﺍﻹﺳﻼﻡ‬ ‫ﻭﺍﻟﻌﺭﻭﺑﺔ‬
‫ﻭﺍﻷﻣﺎﺯﻳﻐﻳﺔ‪.‬‬‫ﻭﺗﻣﺗﺩ‬ ‫ﺟﺫﻭﺭ‬ ‫ﻧﺿﺎﻟﻬﺎ‬ ‫ﺍﻟﻳﻭﻡ‬ ‫ﻓﻲ‬ ‫ﺷﺗﻰ‬ ‫ﺍﻟﻣﻳﺎﺩﻳﻥ‬ ‫ﻓﻲ‬ ‫ﻣﺎﺿﻲ‬ ‫ﺃﻣﺗﻬﺎ‬ ‫ﺍﻟﻣﺟﻳﺩ‬ ‫‪.‬‬
‫ﻟﻘﺩ‬‫ﺗﺟﻣﻊ‬ ‫ﺍﻟﺷﻌﺏ‬ ‫ﺍﻟﺟﺯﺍﺋﺭﻱ‬ ‫ﻓﻲ‬ ‫ﻅﻝ‬ ‫ﺍﻟﺣﺭﻛﺔ‬ ‫ﺍﻟﻭﻁﻧﻳﺔ‪،‬‬ ‫ﺛﻡ‬ ‫ﺍﻧﺿﻭﻯ‬ ‫ﺗﺣﺕ‬ ‫ﻟﻭﺍء‬ ‫ﺟﺑﻬﺔ‬ ‫ﺍﻟﺗﺣﺭﻳﺭ‬ ‫ﺍﻟﻭﻁﻧﻲ‪،‬‬ ‫ﻭﻗﺩﻡ‬
‫ﺗﺿﺣﻳﺎﺕ‬‫ﺟﺳﺎﻣﺎ‬ ‫ﻣﻥ‬ ‫ﺃﺟﻝ‬ ‫ﺃﻥ‬ ‫ﻳﺗﻛﻔﻝ‬ ‫ﺑﻣﺻﻳﺭﻩ‬ ‫ﺍﻟﺟﻣﺎﻋﻲ‬ ‫ﻓﻲ‬ ‫ﻛﻧﻑ‬ ‫ﺍﻟﺣﺭﻳﺔ‬ ‫ﻭﺍﻟﻬﻭﻳﺔ‬ ‫ﺍﻟﺛﻘﺎﻓﻳﺔ‬ ‫ﺍﻟﻭﻁﻧﻳﺔ‬ ‫ﺍﻟﻣﺳﺗﻌﺎﺩﺗﻳﻥ‪،‬‬
‫ﻭﻳﺷﻳﺩ‬‫ﻣﺅﺳﺳﺎﺗﻪ‬ ‫ﺍﻟﺩﺳﺗﻭﺭﻳﺔ‬ ‫ﺍﻟﺷﻌﺑﻳﺔ‬ ‫ﺍﻷﺻﻳﻠﺔ‬ ‫‪.‬‬
‫ﻭﻗﺩ‬‫ﺗﻭﺟﺕ‬ ‫ﺟﺑﻬﺔ‬ ‫ﺍﻟﺗﺣﺭﻳﺭ‬ ‫ﺍﻟﻭﻁ‬ ‫ﻧﻲ‬‫ﻣﺎ‬ ‫ﺑﺫﻟـﻪ‬ ‫ﺧﻳﺭﺓ‬ ‫ﺃﺑﻧﺎء‬ ‫ﺍﻟﺟﺯﺍﺋﺭ‬ ‫ﻣﻥ‬ ‫ﺗﺿﺣﻳﺎﺕ‬ ‫ﻓﻲ‬ ‫ﺍﻟﺣﺭﺏ‬ ‫ﺍﻟﺗﺣﺭﻳﺭﻳﺔ‬
‫ﺍﻟﺷﻌﺑﻳﺔ‬‫ﺑﺎﻻﺳﺗﻘﻼﻝ‪،‬‬ ‫ﻭﺷﻳﺩﺕ‬ ‫ﺩﻭﻟﺔ‬ ‫ﻋﺻﺭﻳﺔ‬ ‫ﻛﺎﻣﻠﺔ‬ ‫ﺍﻟﺳﻳﺎﺩﺓ‬ ‫‪.‬‬
‫ﺇﻥ‬‫ﺇﻳﻣﺎﻥ‬ ‫ﺍﻟﺷﻌﺏ‬ ‫ﺑﺎﻻﺧﺗﻳﺎﺭﺍﺕ‬ ‫ﺍﻟﺟﻣﺎﻋﻳﺔ‬ ‫ﻣﻛﻧﻪ‬ ‫ﻣﻥ‬ ‫ﺗﺣﻘﻳﻕ‬ ‫ﺍﻧﺗﺻﺎﺭﺍﺕ‬ ‫ﻛﺑﺭﻯ‪،‬‬ ‫ﻁﺑﻌﺗﻬﺎ‬ ‫ﺍﺳﺗﻌﺎﺩﺓ‬ ‫ﺍﻟﺛﺭﻭﺍﺕ‬
‫ﺍﻟﻭﻁﻧﻳﺔ‬‫ﺑﻁﺎﺑﻌﻬﺎ‪،‬‬ ‫ﻭﺟﻌﻠﺗﻬﺎ‬ ‫ﺩﻭﻟﺔ‬ ‫ﻓﻲ‬ ‫ﺧﺩﻣﺔ‬ ‫ﺍﻟﺷﻌﺏ‬ ‫ﻭﺣﺩﻩ‪،‬‬ ‫ﺗﻣﺎ‬ ‫ﺭﺱ‬‫ﺳﻠﻁﺎﺗﻬﺎ‬ ‫ﺑﻛﻝ‬ ‫ﺍﺳﺗﻘﻼﻟﻳﺔ‪،‬‬ ‫ﺑﻌﻳﺩﺓ‬ ‫ﻋﻥ‬ ‫ﺃﻱ‬ ‫ﺿﻐﻁ‬
‫ﺧﺎﺭﺟﻲ‬‫‪.‬‬
‫ﺇﻥ‬‫ﺍﻟﺷﻌﺏ‬ ‫ﺍﻟﺟﺯﺍﺋﺭﻱ‬ ‫ﻧﺎﺿﻝ‬ ‫ﻭﻳﻧﺎﺿﻝ‬ ‫ﺩﻭﻣﺎ‬ ‫ﻓﻲ‬ ‫ﺳﺑﻳﻝ‬ ‫ﺍﻟﺣﺭﻳﺔ‬ ‫ﻭﺍﻟﺩﻳﻣﻘﺭﺍﻁﻳﺔ‪،‬‬ ‫ﻭﻳﻌﺗﺯﻡ‬ ‫ﺃﻥ‬ ‫ﻳﺑﻧﻲ‬ ‫ﺑﻬﺫﺍ‬ ‫ﺍﻟﺩﺳﺗﻭﺭ‬
‫ﻣﺅﺳﺳﺎﺕ‬‫ﺩﺳﺗﻭﺭﻳﺔ‪،‬‬ ‫ﺃﺳﺎﺳﻬﺎ‬ ‫ﻣﺷﺎﺭﻛﺔ‬ ‫ﻛﻝ‬ ‫ﺟﺯﺍﺋﺭﻱ‬ ‫ﻭﺟﺯﺍﺋﺭﻳﺔ‬ ‫ﻓﻲ‬ ‫ﺗﺳﻳﻳﺭ‬ ‫ﺍﻟﺷﺅﻭﻥ‬ ‫ﺍﻟﻌﻣﻭﻣﻳﺔ‪،‬‬ ‫ﻭﺍﻟﻘﺩﺭﺓ‬ ‫ﻋﻠﻰ‬
‫ﺗﺣﻘﻳﻕ‬‫ﺍﻟﻌﺩﺍﻟﺔ‬ ‫ﺍﻻﺟﺗﻣﺎﻋﻳﺔ‪،‬‬ ‫ﻭﺍﻟﻣﺳﺎﻭﺍﺓ‪،‬‬ ‫ﻭﺿﻣﺎﻥ‬ ‫ﺍﻟﺣﺭﻳﺔ‬ ‫ﻟﻛﻝ‬ ‫ﻓﺭﺩ‬ ‫‪.‬‬"""


# 487 characters
text_3 = """Article Premier : Tout opérateur de télécommunication et TIC, exploitant de réseau privé et fournisseur
d’équipements terminaux doit s’acquitter du paiement de taxe intitulée « Taxe de régulation ». Elle est
calculée sur son chiffre d’affaires hors taxes comptabilisé relatif aux activités de des télécommunications et
TIC, et réalisé durant un exercice fiscal. La taxe de régulation est perçue au profit du budget de l’Agence de
régulation prévue par la Loi 2005-023 du 17 octobre 2005."""


# 1537 characters
text_4 = """Article Premier : Tout opérateur de télécommunication et TIC, exploitant de réseau privé et fournisseur
d’équipements terminaux doit s’acquitter du paiement de taxe intitulée « Taxe de régulation ». Elle est
calculée sur son chiffre d’affaires hors taxes comptabilisé relatif aux activités de des télécommunications et
TIC, et réalisé durant un exercice fiscal. La taxe de régulation est perçue au profit du budget de l’Agence de
régulation prévue par la Loi 2005-023 du 17 octobre 2005.
Article 2 : Le chiffre d’affaires est constitué par la vente d’équipements terminaux de télécommunications
et/ou les revenus générés par la fourniture au public de services de télécommunications et TIC, et s’entend
du montant des affaires réalisées avec les tiers dans l’exercice de l’activité professionnelle, normale et
courante de l’entreprise.
Article 3 : Tout opérateur est tenu de déclarer à l’Agence de régulation son Chiffre d’Affaires Hors Taxes
Comptabilisé, arrêté au 31 décembre de chaque année, au plus tard le 30 avril de l’année suivante. Chaque
déclaration doit être établie suivant un modèle défini par l’Agence de régulation. Elle doit être certifiée par un
expert comptable et financier pour les opérateurs soumis au contrôle d’un commissaire aux comptes par la
réglementation en vigueur.
Article 7 : Jusqu’à la mise en place officielle de l’Agence de régulation prévue par la Loi n°2005-023 du 17
octobre 2005, la taxe de régulation est perçue au profit l’Office Malagasy d’Etudes et de Régulation des
Télécommunications (OMERT)."""


# 519 characters
text_5 = """Artículo 3°.- Definiciones. Para los efectos del presente reglamento, se
entiende por:
a) Actos administrativos: Aquéllos señalados en el artículo 3° de la ley N°
19.880, que establece las Bases de los Procedimientos Administrativos que rigen los
actos de los órganos de la Administración del Estado.
b) Autoridad, jefatura o jefe superior del órgano o servicio de la
Administración del Estado: Es la autoridad con competencia comunal, provincial,
regional o, en su caso, el jefe superior del servicio a nivel nacional."""


# 1425 characters
text_6 = """c) Datos sensibles: Los datos personales que se refieren a las características
físicas o morales de las personas o a hechos o circunstancias de su vida privada o
intimidad, tales como los hábitos personales, el origen social, las ideologías y
opiniones políticas, las creencias o convicciones religiosas, los estados de salud
físicos o psíquicos y la vida sexual.
d) Derecho de Acceso a la Información: Toda persona tiene derecho a solicitar y
recibir información que obre en poder de cualquier órgano de la Administración del
Estado, en la forma y condiciones que establece la ley.
e) Documentos: Todo escrito, correspondencia, memorándum, plano, mapa, dibujo,
diagrama, documento gráfico, fotografía, microforma, grabación sonora, video,
dispositivo susceptible de ser leído mediante la utilización de sistemas
mecánicos, electrónicos o computacionales y, en general, todo soporte material que
contenga información, cualquiera sea su forma física o características, así como
las copias de aquéllos.
f) Órganos y servicios públicos creados para el cumplimiento de la función
administrativa: Los órganos o servicios de la Administración del Estado señalados
en el inciso 2º del artículo 1º de la Ley Orgánica Constitucional de Bases
Generales de la Administración del Estado, cuyo texto refundido, coordinado y
sistematizado está contenido en el DFL. Nº 1/19.653, de 2001, del Ministerio
Secretaria General de la Presidencia."""


# 508 characters
text_7 = """В некоторых алгоритмах машинного обучения в роли опыта выступает не только
фиксированный набор данных. Так, алгоритмы обучения с подкреплением взаимодействуют с окружающей средой, так что между системой обучения и ее опытом образуется контур с обратной связью. Такие алгоритмы выходят за рамки нашей книги.
Дополнительные сведения об обучении с подкреплением см. в работах Sutton and
Barto (1998) или Bertsekas and Tsitsiklis (1996), а о подходе к этой теме на основе
глубокого обучения – Mnih et al. (2013)."""


# 1513 characters
text_8 = """Хотя обучение с учителем и без учителя – понятия, не формализованные и не разделенные четкой границей, они все же помогают приблизительно распределить по
категориям некоторые задачи, решаемые в машинном обучении. Принято относить
задачи регрессии, классификации и структурного вывода к обучению с учителем,
а задачу оценивания плотности – к обучению без учителя.
Возможны и другие варианты парадигмы обучения. Например, в случае обучения
с частичным привлечением учителя одни примеры снабжены метками, а другие – нет.
В многовариантном обучении вся совокупность примеров помечается как содержащая или не содержащая пример класса, но отдельные ее элементы никак не помечаются. Недавний пример многовариантного обучения глубоких моделей см. в работе
Kotzias et al. (2015).
В некоторых алгоритмах машинного обучения в роли опыта выступает не только
фиксированный набор данных. Так, алгоритмы обучения с подкреплением взаимодействуют с окружающей средой, так что между системой обучения и ее опытом образуется контур с обратной связью. Такие алгоритмы выходят за рамки нашей книги.
Дополнительные сведения об обучении с подкреплением см. в работах Sutton and
Barto (1998) или Bertsekas and Tsitsiklis (1996), а о подходе к этой теме на основе
глубокого обучения – Mnih et al. (2013).
В большинстве алгоритмов машинного обучения опытом является просто набор
данных, который можно описать разными способами. Но в любом случае набор данных – это совокупность примеров, каждый из которых является совокупностью признаков."""


def benchmark():
    ip_address = MlCloudConnector().get_ip()
    texts = [text_1, text_2, text_3, text_4, text_5, text_6, text_7, text_8]
    base_content = f"""Please translate the following text into English. Follow these guidelines:
1. Maintain the original layout and formatting.
2. Translate all text accurately without omitting any part of the content.
3. Preserve the tone and style of the original text.
4. Do not include any additional comments, notes, or explanations in the output; provide only the translated text.

Here is the text to be translated:
    """
    total_time_start = time()
    for i in range(3):
        iteration_time_start = time()
        for text in tqdm(texts):
            client = Client(host=f"http://{ip_address}:{TRANSLATIONS_PORT}")
            translation_content = base_content + "\n\n" + text
            response = client.chat(
                model="aya:35b",
                messages=[
                    {
                        "role": "user",
                        "content": translation_content,
                    }
                ],
            )
        iteration_time = round(time() - iteration_time_start, 2)
        print(f"Iteration {i+1} finished in {iteration_time} seconds.")
    total_time = round(time() - total_time_start, 2)
    print(f"All rounds finished in {total_time} seconds")
    print("[Iteration 1 also includes model loading time]")


if __name__ == "__main__":
    benchmark()
