# Azure AI Use-Case Governance Demo

[![tests](https://github.com/bianka20010221-crypto/azure-ai-usecase-governance-demo/actions/workflows/tests.yml/badge.svg)](https://github.com/bianka20010221-crypto/azure-ai-usecase-governance-demo/actions/workflows/tests.yml)

Tesztelhető Azure Functions referenciaalkalmazás AI/ML use case-ek első szakmai és governance-értékeléséhez. A szolgáltatás validálja az üzleti célt, az adatbesorolást, a döntési hatást és az emberi jóváhagyást, majd magyarázható javaslatot ad a következő lépésre.

## English summary

A testable Azure Functions reference application for the initial governance assessment of AI/ML use cases. It validates business ownership, data classification, decision impact and human approval, then returns an explainable recommendation. An optional Microsoft Foundry model creates a stakeholder summary but cannot override deterministic controls.

## Mit bizonyít a projekt?

- Azure Functions Python v2 programozási modell;
- HTTP API és strukturált validáció;
- Microsoft Foundry/Azure OpenAI opcionális integráció;
- Microsoft Entra ID és `DefaultAzureCredential` alapú, kulcsmentes hitelesítési minta;
- Application Insights-kompatibilis strukturált naplózás;
- emberi jóváhagyás és determinisztikus governance-kontroll;
- automatikus GitHub Actions tesztelés;
- titokmentes konfigurációs minta.

## Döntési kimenetek

| Eredmény | Jelentés |
|---|---|
| `prototype` | Kis, mérhető prototípus fiktív adatokkal |
| `limited-pilot` | Korlátozott felhasználói kör és előre definiált mérőszámok |
| `controlled-poc` | Adatvédelmi, biztonsági és tulajdonosi kontrollal végzett PoC |
| `blocked` | A megvalósítás nem folytatható a hiányzó kontroll pótlásáig |

## Helyi teszt

```bash
python -m unittest discover -s tests -v
```

Az üzleti döntési mag külső szolgáltatás nélkül tesztelhető. Az Azure Function futtatásához telepítsd az Azure Functions Core Toolst, másold a `local.settings.example.json` fájlt `local.settings.json` névre, majd használd a `func start` parancsot.

## Biztonság

- Nincs kulcs vagy valódi végpont a repositoryban.
- Az opcionális modellhívás Entra ID-alapú hitelesítést használ.
- A modell csak összefoglal, a governance-döntést nem módosíthatja.
- A naplózás nem tartalmazza a beküldött üzleti szöveget.
- Az HTTP végpont alapértelmezetten Function-szintű engedélyezést kér.

Részletesebben: [architektúra](docs/architecture.md) · [üzemeltetési ellenőrzőlista](docs/operations.md)

## Fontos

Ez egy portfóliócélú referenciaimplementáció fiktív példaadattal. Nincs élő Azure-erőforráshoz kapcsolva, ezért költséget sem hoz létre és nem állít valótlan üzemeltetési tapasztalatot.
