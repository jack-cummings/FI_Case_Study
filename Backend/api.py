from fastapi import FastAPI, Request, BackgroundTasks, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from retrieve import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class questionObj(BaseModel):
    text: str

@app.post("/inference")
async def inference(question: questionObj):
    # try:
    #     print(question.text)
    #     answer = get_answer(question.text)
    #     return answer

    # except Exception as e:
    #     print(e)
    #     return {'content':f'Error:{e}','url':'no url'}
    
    return {'content': "Tacos originate from Mexico. They are a traditional Mexican dish consisting of a small hand-sized corn or wheat tortilla topped with a filling. The tortilla is then folded around the filling and eaten by hand. The fillings can vary and include beef, pork, chicken, seafood, beans, vegetables, and cheese. They are often garnished with various condiments like salsa, guacamole, or sour cream, and vegetables such as lettuce, onion, tomatoes, and chiles.",
    'context': """A taco (US: /ˈtɑːkoʊ/, UK: /ˈtækoʊ/, Spanish: [ˈtako]) is a traditional Mexican food consisting of a small hand-sized corn- or wheat-based tortilla topped with a filling. The tortilla is then folded around the filling and eaten by hand. A taco can be made with a variety of fillings, including beef, pork, chicken, seafood, beans, vegetables, and cheese, allowing for great versatility and variety. They are often garnished with various condiments, such as salsa, guacamole, or sour cream, and vegetables, such as lettuce, onion, tomatoes, and chiles. Tacos are a common form of antojitos, or Mexican street food, which have spread around the world.

Tacos can be contrasted with similar foods such as burritos, which are often much larger and rolled rather than folded; taquitos, which are rolled and fried; or chalupas/tostadas, in which the tortilla is fried before filling.

Etymology
The origins of the taco are not precisely known, and etymologies for the culinary usage of the word are generally theoretical.[1][2] Taco in the sense of a typical Mexican dish comprising a maize tortilla folded around food is just one of the meanings connoted by the word, according to the Real Academia Española, publisher of Diccionario de la Lengua Española.[3] This meaning of the Spanish word "taco" is a Mexican innovation,[2] but the word "taco" is used in other contexts to mean "wedge; wad, plug; billiard cue; blowpipe; ramrod; short, stocky person; [or] short, thick piece of wood."[3] The etymological origin of this sense of the word is Germanic and has cognates in other European languages, including the French word tache and the English word "tack".[4]

In Spain, the word "taco" can also be used in the context of tacos de jamón [es]: these are diced pieces of ham, or sometimes bits and shavings of ham leftover after a larger piece is sliced.[5] They can be served on their own as tapas or street food, or can be added to other dishes such as salmorejo, omelettes, stews, empanadas, or melón con jamón [es].[6][7][8]

According to one etymological theory, the culinary origin of the term "taco" in Mexico can be traced to its employment, among Mexican silver miners, as a term signifying "plug." The miners used explosive charges in plug form, consisting of a paper wrapper and gunpowder filling.[1]

Indigenous origins are also proposed. One possibility is that the word derives from the Nahuatl word tlahco, meaning "half" or "in the middle",[9] in the sense that food would be placed in the middle of a tortilla.[10] Furthermore, dishes analogous to the taco were known to have existed in Pre-Columbian society—for example, the Nahuatl word tlaxcalli (a type of corn tortilla).[9]

History
There is significant debate about the origins of the taco in Mexico, with some arguing that the taco predates the arrival of the Spanish in Mexico, since there is anthropological evidence that the indigenous people living in the lake region of the Valley of Mexico traditionally ate tacos filled with small fish.[11] Writing at the time of the Spanish conquistadors, Bernal Díaz del Castillo documented the first taco feast enjoyed by Europeans, a meal which Hernán Cortés arranged for his captains in Coyoacán.[12][13] Others argue that the advent of the taco is much more recent, with one of the more popular theories being that the taco was invented by silver miners in the 18th century,[14]

One of the oldest mentions of a taco comes from an 1836 cookbook —Nuevo y sencillo arte de cocina, reposteria y refrescos— by Antonia Carrillo; in a recipe for a rolled pork loin (lomo de cerdo enrollado), she instructs the readers to roll the loin like they would a “taco de tortilla” or tortilla taco.[15]

Another mention of the word taco comes from the novel —El hombre de la situación (1861)— by Mexican writer Manuel Payno:[16]
“They surrounded the father's bed, and he, putting a pillow on his legs, which served as a table, began to give the example, and a pleasant gathering was formed, which was completed by the mother, who always entered last, waving with one hand (from right to left) a large cup of white atole, while with the other she carried, right to her mouth, a tortilla taco filled with a spread of red chile.

These instances predate the theory that the first mention of the word "taco" in Mexico was in the 1891 novel Los bandidos de Río Frío by Manuel Payno.[17]

Traditional variations
There are many traditional varieties of tacos:


Tacos al pastor made with adobada meat
Tacos al pastor ("shepherd style") or tacos de adobada are made of thin pork steaks seasoned with adobo seasoning, then skewered and overlapped on one another on a vertical rotisserie cooked and flame-broiled as it spins.[18][19]
Tacos de asador ("spit" or "grill" tacos) may be composed of any of the following: carne asada tacos; tacos de tripita ("tripe tacos"), grilled until crisp; and, chorizo asado (traditional Spanish-style sausage). Each type is served on two overlapped small tortillas and sometimes garnished""",
'url': 'https://en.wikipedia.org/wiki/Taco'}


if __name__ == '__main__':
    uvicorn.run(app, port=4242, host='0.0.0.0')