import logging
import os
from pathlib import Path

import graypy

SRC_PATH = Path(__file__).parent.absolute()
ROOT_PATH = Path(__file__).parent.parent.absolute()
MODEL = "aya:35b"
TRANSLATIONS_PORT = 11434
# TRANSLATIONS_PORT = 8080
LANGUAGES_SHORT = ["en", "fr", "es", "ru", "ar", "sp"]
LANGUAGES = ["English", "French", "Spanish", "Russian", "Arabic", "Spanish"]

TASK_QUEUE_NAME = "translation_tasks"
RESULTS_QUEUE_NAME = "translation_results"

GRAYLOG_IP = os.environ.get("GRAYLOG_IP")
REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")

handlers = [logging.StreamHandler()]

if GRAYLOG_IP:
    handlers.append(graypy.GELFUDPHandler(GRAYLOG_IP, 12201, localname="pdf_metadata_extraction"))

logging.root.handlers = []
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=handlers)
service_logger = logging.getLogger(__name__)
service_logger.setLevel(logging.WARNING)

prompt_1 = (
        "Translate the below text to {translation_task.language_to}, "
        "keep the layout, do not skip any text, do not output anything else besides translation:"
    )


prompt_2 = """Please translate the following text into {translation_task.language_to}. Follow these guidelines:
1. Maintain the original layout and formatting.
2. Translate all text accurately without omitting any part of the content.
3. Preserve the tone and style of the original text.
4. Do not include any additional comments, notes, or explanations in the output; provide only the translated text.

Here is the text to be translated:
"""


prompt_3 = """As a professional translator with expertise in {translation_task.language_to}, please translate the following text. Your translation should:
1. Preserve the original layout and formatting.
2. Translate all content accurately without omitting any part.
3. Maintain the original tone and style to reflect the same meaning and emotion.

Here is the text to be translated:
"""


prompt_4 = """Task: Translate the following text into {translation_task.language_to}.
Requirements:
1. Maintain the original layout and formatting.
2. Ensure every part of the text is accurately translated without omissions.
3. Preserve the tone and style of the original content.
Output: Only the translated text, with no additional comments or notes.

Text to be translated:
"""



cejil_1_page = """
RESOLUCIÓN DEL PRESIDENTE DE LA
CORTE INTERAMERICANA DE DERECHOS HUMANOS
DE 17 DE DICIEMBRE DE 2018
CASO ARROM SUHURT Y OTROS VS. PARAGUAY
VISTO:
1.
El escrito de sometimiento del caso y el Informe de Fondo de la Comisión Interamericana
de Derechos Humanos (en adelante “la Comisión Interamericana” o “la Comisión”); el escrito
de solicitudes, argumentos y pruebas (en adelante el “escrito de solicitudes y argumentos”)
del representante de las presuntas víctimas (en adelante “el representante”); el escrito de
excepciones preliminares y de contestación al sometimiento del caso y al escrito de solicitudes
y argumentos (en adelante “escrito de contestación”) de la República del Paraguay (en
adelante “Paraguay” o “el Estado”), así como los escritos de observaciones a las excepciones
preliminares interpuestas por el Estado presentados por la Comisión Interamericana y el
representante.
2.
Las listas definitivas de declarantes presentadas por el Estado, el representante, la
Comisión y las correspondientes observaciones a dichas listas presentadas por las partes, la
Comisión y los peritos recusados.
3.
La nota de Secretaría de 24 de octubre de 2018 relativa a la procedencia del Fondo de
Asistencia Legal de Víctimas de la Corte Interamericana de Derechos Humanos (en adelante
“Fondo de Asistencia Legal de Víctimas”).
CONSIDERANDO QUE:
1.
El ofrecimiento y la admisión de la prueba, así como la citación de declarantes se
encuentran regulados en los artículos 35.1.f, 40.2.c, 41.1.c, 46, 47, 48, 50, 52.3, 57 y 58 del
Reglamento de la Corte Interamericana de Derechos Humanos (en adelante “la Corte
Interamericana”, “la Corte” o “el Tribunal”).
2.
La Comisión ofreció una declaración pericial. El representante ofreció treinta y un
declaraciones testimoniales y una pericial. El Estado ofreció las declaraciones de cuatro
testigos y de dos peritos.
3.
La Corte garantizó a las partes el derecho de defensa respecto de los ofrecimientos
probatorios oportunamente realizados. La Comisión señaló no tener observaciones. El Estado
recusó al perito propuesto por la Comisión, objetó la admisibilidad de su dictamen y presentó
diversas objeciones respecto a las declaraciones testimoniales ofrecidas por el representante.
Por su parte, el representante recusó a dos peritos propuestos por el Estado y presentó
objeciones respecto a los testigos propuestos por el Estado.
4.
En cuanto a la prueba pericial y testimonial ofrecida por las partes que no ha sido
objetada, esta Presidencia considera conveniente recabarla. Por consiguiente, se admiten las
declaraciones testimoniales de Juan Francisco Arrom Suhurt, Cristina Haydée Arrom Suhurt,
Raúl Marín, Anuncio Martí Méndez, Aníbal Emery, María Auxiliadora Arrom de Orrego,
"""

cejil_2_page = cejil_1_page + """ Esperanza Martínez, Carlos Portillo, Mario Torres, Liza Liana Larriera Rojas, Gloria Elizabeth
Blanco, Carmen Edilia Arrom de Cabello, Carmen Marina Arrom Suhurt, María Cristina Martí
Méndez, Marta Ramona Martí de Páez, Elena Méndez Vda. de Martí y Paulo Ezequias de Jesus 1 ,
así como el peritaje de Marcelo Kimati Dias 2 , todos ofrecidos por el representante.
5.
A continuación el Presidente examinará en forma particular: a) el desistimiento tácito
de declarantes ofrecidos por el representante; b) la recusación y objeciones del Estado
respecto a la declaración pericial propuesta por la Comisión c) la recusación del representante
a los peritos ofrecidos por el Estado; d) las observaciones y objeciones del representante a
testigos ofrecidos por el Estado; e) las observaciones y objeciones del Estado a la declaración
de un testigo ofrecido por el representante, y f) la aplicación del Fondo de Asistencia Legal de
Víctimas ante la Corte.
A.
Desistimiento tácito de declarantes ofrecidos por el representante
6.
El Estado solicitó que se desestimaran las declaraciones ofrecidas por el representante
que no fueron confirmadas en la lista definitiva de declarantes. El Presidente constata que, en
el escrito de solicitudes y argumentos, el representante ofreció las declaraciones de doce
personas sin que fueran confirmadas en su lista definitiva de declarantes 3 . De conformidad
con el artículo 46.1 del Reglamento, el momento procesal oportuno para que las partes
confirmen o desistan de las declaraciones ofrecidas en su escrito de solicitudes y argumentos
o en su escrito de contestación es en la lista definitiva solicitada por el Tribunal. Por tanto, al
no confirmar las declaraciones mencionadas, el representante desistió de las mismas en la
debida oportunidad procesal. En virtud de lo anterior, el Presidente toma nota de dicho
desistimiento.
B.
7.
Recusación y objeciones del Estado respecto a la declaración pericial
propuesta por la Comisión
La Comisión ofreció el dictamen pericial de Víctor Madrigal-Borloz para declarar sobre:
los estándares probatorios aplicables en el derecho internacional de los derechos humanos
para establecer la existencia de tortura y/o desaparición forzada en un caso particular. El
perito tomará en cuenta las implicaciones probatorias y el alcance de la responsabilidad
internacional del Estado en supuestos de incumplimiento del deber de investigar con debida
diligencia los indicios de participación estatal en los hechos denunciados. Además, el perito
se referirá a los estándares internacionales relevantes para calificar ciertos hechos como
desaparición forzada, aun cuando la víctima aparece con vida con posterioridad.
Finalmente, el perito podrá referirse a los hechos del caso a modo de ejemplificar los
aspectos desarrollados en el peritaje.
La Comisión fundamentó el ofrecimiento de la pericia, estimando que el caso presenta
cuestiones que afectan gravemente el orden público interamericano. Concretamente indicó
"""


cejil_3_page = cejil_2_page + """ que la Corte podrá profundizar en su jurisprudencia sobre casos de desaparición forzada de
personas y de tortura, fuera de un contexto dictatorial o de conflicto armado con violaciones
sistemáticas de derechos humanos.
8.
El Estado presentó una recusación al peritaje ofrecido por la Comisión, alegando que:
(i) el señor Víctor Madrigal-Borloz durante el período de agosto del 2004 a diciembre del 2006
ocupó el cargo de jefe de litigios de la Comisión Interamericana, cargo en el cual supervisó
todas las comunicaciones legales de la Comisión y coordinó todas las comparecencias ante la
Corte, como asimismo fue responsable del desarrollo de la estrategia en casos, entre otras
funciones; (ii) durante gran parte del trámite de admisibilidad de esta petición el perito
propuesto tenía una relación de subordinación funcional con la Comisión, al ostentar un cargo
que le permitió conocer el contenido de todas las peticiones o denuncias formuladas ante
dicho órgano , incluyendo la petición inicial en el caso concreto, y (iii) ha tenido una directa
opinión y participación en los dictámenes que sirvieron de base a la Comisión para formular
el informe de admisibilidad dictado en la presente petición. En vista de lo anterior, el Estado
estimó haber “presentado elementos fácticos y argumentos sólidos que muestran el
acaecimiento de los supuestos de recusación previstas en el art. 48, incisos c) y d) del
Reglamento”, por lo que solicitó a la Corte rechazar la prueba pericial propuesta por la
Comisión “ante la patente falta de objetividad del perito propuesto”.
9.
Por otro lado, y de manera subsidiaria a la solicitud de recusación, el Estado alegó que
la Comisión no ha expuesto ninguna razón coherente y plausible que fundamente la
excepcionalidad de la admisión de la pericia propuesta, ni mucho menos ha demostrado la
supuesta afectación relevante del orden público interamericano de Derechos Humanos”.
Además indicó que “es innecesaria e improcedente que una persona en su calidad de supuesto
‘perito’, coadyuve a que la Corte IDH profundice en su jurisprudencia sobre casos de
desaparición forzada de personas y tortura”.
10. Respecto a la recusación presentada en su contra, el señor Madrigal-Borloz señaló que
“la petición inicial del presente caso fue abierta a trámite mediante la notificación al Estado
de Paraguay el 20 de mayo de 2003”. Por lo tanto, “el estudio inicial y la decisión de apertura
a trámite de la petición tuvo lugar antes de [su] incorporación a la Secretaría Ejecutiva” de la
Comisión. El perito señaló que como funcionario de la Secretaría Ejecutiva nunca estuvo a
cargo de peticiones en etapa de admisibilidad o casos en etapa de fondo. Agregó que “en
ningún momento tuv[o] conocimiento ni emit[ió] opinión de naturaleza alguna sobre el
presente caso en el cual se [le] ha ofrecido como perito durante [su] vinculación con la
Secretaría Ejecutiva”. También señaló que los supuestos para que sea procedente la causal
de recusación prevista en el artículo 48.1.c no están presentes en este caso.
11. El artículo 48.1.d del Reglamento dispone que los peritos podrán ser recusados por “ser
o haber sido funcionario de la Comisión con conocimiento del caso en litigio en que se solicita
su peritaje”. Esta Presidencia ha constatado que de la hoja de vida del perito se desprende
que fungió como “Jefe de Litigio” de la Comisión ante la Corte entre agosto de 2004 a
diciembre de 2006, y desde enero de 2007 hasta septiembre del 2013 ocupó el cargo de “Jefe
de Sección de Registro y Especialista Principal de Derechos Humanos” de la Comisión, donde
supervisaba el estudio inicial realizado a las peticiones. En el presente caso, la Comisión dio
trámite a la petición el 20 de mayo del 2003 4 , por lo que el estudio inicial de la petición se
realizó años antes que el perito fuese el encargado de supervisar el estudio inicial de las
peticiones. Además, se desprende de la hoja de vida del perito que durante su trabajo en la
Secretaría Ejecutiva no trabajó en las decisiones de admisibilidad y fondo de casos, así como"""