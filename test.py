from datetime import datetime, timedelta

pnchet = []
chet_monday = datetime.strptime("06.09.2021", '%d.%m.%Y') # первый четный понедельник
for _ in range(20):
	pnchet.append(chet_monday.strftime("%d.%m"))
	chet_monday = chet_monday + timedelta(days=14)

print(pnchet)