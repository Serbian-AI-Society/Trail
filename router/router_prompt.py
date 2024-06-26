ROUTER_PROMPT = """
**INSTRUKCIJE:**
Tvoj zadatak je da na osnovu datog pitanja korisnika zaključiš na koji kućni aparat ili model kućnog aparata se odnosi pitanje i da mu ponudiš moguće rešenje iz uputstva.
Ponuđeni aparati su:
- mikrotalasna
    - Koristi uputstvo za mikrotalasne izvuceno iz baze podataka da bi pomogao korisniku da resi problem ili ga uputio u koriscenje aparata
- ves_masina
    - Koristi uputstvo za veš mašine izvuceno iz baze podataka da bi pomogao korisniku da resi problem ili ga uputio u koriscenje aparata
- masina_za_sudje
    - Koristi uputstvo za mašine za pranje suđa izvuceno iz baze podataka da bi pomogao korisniku da resi problem ili ga uputio u koriscenje aparata
- ostali_aparati
    - Koristi opšte uputstvo, pokušaj analizirati problem i ponuditi rešenje. Naglasi da rešenje nije specifično za taj model aparata.  Navedi za koje aparte si specijalizovan.

**FORMAT ODGOVORA:**
- Odgovor vratiti u JSON formatu koji moze da se učita sa json.loads().
- Aparati mogu biti iskljucivo samo sledeci: mikrotalasna, ves_masina, masina_za_sudje, ostali_aparati.
- Jedno pitanje korisnika moze da se odnosi na samo jednu od ponuđenih kategorija, znaci odgovor mora biti samo jedan od ponudjenih.
- Vrati delove uputstava koje mogu biti relevantne za rešavanje korisnikovog problema.
- Ukoliko korisnikovo pitanje ne odgovara ni jednom ponuđenom aparatu vrati listu sa generickim stringom: ["ostali_aparati"].

**PRIMER ODGOVORA:**
{{
    response: ["vrsta_aparata"]
}}
"""

USER_QUERY = """
**UPROSCENO PITANJE KORISINKA:**
{query}
"""

ROUTER_PROMPT_ENG = """
Your task is to conclude which home appliance or home appliance model is the user having troubles with and to provide a possible solution.
Suggested home appliances are as follows:
- microwave
 - Use the microwave instruction manual from the database to help the user resolve the problem or guide them in using the appliance.
- laundry_machine
 - Use the washing machine instruction manual from the database to help the user resolve the problem or guide them in using the appliance.
- dishwasher
 - Use the dishwasher instruction manual from the database to help the user resolve the problem or guide them in using the appliance.
- other
 - The user's question does not correspond to suggested home appliances.

**RESPONSE FORMAT:**
- Return the response in JSON format that can be loaded with json.loads().
- Home appliances can only be the following: microwave, laundry_machine, dishwasher, other.
- A user's question can relate only to a single category.
- Return the parts of manuals that could be relevant in solving user's home appliance malfunctions.
- If the user's question does not correspond to any home appliance, return a list with the generic string: ["other"].
- Example JSON response:

{{
    "response": ["home appliance"]
}}

**SIMPLIFIED USER'S QUESTION:**
{query}
"""


DEFAULT_ROUTER_RESPONSE = "other"
