{
  "name": "BTP IA - Correctif Modèle 2.5",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "c8f039e9-89af-4d1a-b378-8e77a0a348b0",
        "options": {}
      },
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2.1,
      "position": [
        -1180,
        -60
      ],
      "id": "c06dc184-f9b3-4ecc-9530-b53dbbbabb2e",
      "name": "Webhook",
      "webhookId": "c8f039e9-89af-4d1a-b378-8e77a0a348b0"
    },
    {
      "parameters": {
        "jsCode": "const body = $json.body || $json; \nconst clean = (val) => String(val || \"\").trim();\n\n// 1. Récupération sécurisée du fichier\nconst binaryKeys = Object.keys($binary || {});\n\nif (binaryKeys.length === 0) {\n  throw new Error(\"ERREUR: Aucun fichier binaire reçu par le Webhook.\");\n}\n\n// On prend le premier fichier (peu importe son nom: 'file', 'data', 'attachment')\nconst firstKey = binaryKeys[0];\nconst fileObject = $binary[firstKey];\n\n// 2. Vérification de l'intégrité (est-ce que 'data' existe dedans ?)\nif (!fileObject || !fileObject.data) {\n   throw new Error(\"ERREUR: Le fichier binaire est vide ou invalide (propriété 'data' manquante).\");\n}\n\n// 3. Données Contact\nconst contact = {\n  first_name: clean(body.first_name),\n  last_name:  clean(body.last_name),\n  email:      clean(body.email).toLowerCase(),\n  phone:      clean(body.phone).replace(/\\s+/g, \"\"),\n  address:    clean(body.address),\n  city:       clean(body.city),\n  postal_code:clean(body.postal_code),\n  country:    clean(body.country)\n};\n\n// 4. Sortie Formatée en Tableau (Correction du Bug 'Undefined')\nreturn [\n  {\n    json: {\n      contact,\n      source: \"app_excelia\"\n    },\n    binary: {\n      data: fileObject // On le renomme explicitement en 'data'\n    }\n  }\n];"
      },
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        -960,
        -60
      ],
      "id": "7c07ac40-0dab-415a-8341-673c33246c74",
      "name": "Données normalisées"
    },
    {
      "parameters": {
        "resource": "document",
        "modelId": {
          "__rl": true,
          "value": "models/gemini-2.5-pro",
          "mode": "id",
          "cachedResultName": "models/gemini-2.5-pro"
        },
        "text": "Tu es un extracteur structuré. À partir du PDF, lis UNIQUEMENT le cartouche (zone administrative) et retourne UNIQUEMENT ce JSON :\n{\"plan_title\":string|null,\"scale\":string|null,\"level\":string|null,\"surface_annoncee_m2\":number|null,\"date_plan\":string|null,\"constructeur\":string|null}\nContraintes :\n- Ignore totalement la zone de dessin.\n- \"date_plan\" au format YYYY-MM-DD.\n- Utilise le point pour les décimales.\n- Aucun texte hors JSON.\n",
        "inputType": "binary",
        "binaryPropertyName": "data",
        "options": {
          "maxOutputTokens": 2048
        }
      },
      "type": "@n8n/n8n-nodes-langchain.googleGemini",
      "typeVersion": 1,
      "position": [
        -680,
        -180
      ],
      "id": "87881431-4cfa-4137-be34-5429cdaa76c0",
      "name": "Infos officielles du plan (PDF)",
      "credentials": {
        "googlePalmApi": {
          "id": "jUZkuKOb0zenQCB6",
          "name": "Google Gemini(PaLM) Api account"
        }
      }
    },
    {
      "parameters": {
        "resource": "document",
        "modelId": {
          "__rl": true,
          "value": "models/gemini-2.5-pro",
          "mode": "id",
          "cachedResultName": "models/gemini-2.5-pro"
        },
        "text": "\nRésume le plan en 1000 tokens maximum.\nAnalyse UNIQUEMENT la zone de dessin (ignore le cartouche) et retourne UNIQUEMENT ce JSON minifié :\n{\"surface_totale_m2\":number|null,\n \"surfaces_detaillees\":{\"habitable_m2\":number|null,\"garage_m2\":number|null,\"porche_m2\":number|null},\n \"pieces\":[{\"type\":string,\"surface\":number}],\n \"ouvertures\":[{\"type\":\"fenetre\"|\"porte\"|\"baie\",\"largeur_m\":number|null,\"hauteur_m\":number|null,\"quantite\":number}],\n \"lineaires\":{\"murs_ml\":number|null,\"semelles_ml\":number|null},\n \"qualite_detection\":number}\nContraintes : point pour les décimales ; limite \"pieces\" aux 15 principales. Aucun texte hors JSON.\n",
        "inputType": "binary",
        "binaryPropertyName": "data",
        "options": {
          "maxOutputTokens": 4096
        }
      },
      "type": "@n8n/n8n-nodes-langchain.googleGemini",
      "typeVersion": 1,
      "position": [
        -680,
        60
      ],
      "id": "b0d88481-1e7d-4117-a210-640dd70ecb3a",
      "name": "IA #2 – Vision Parser",
      "credentials": {
        "googlePalmApi": {
          "id": "jUZkuKOb0zenQCB6",
          "name": "Google Gemini(PaLM) Api account"
        }
      }
    }
  ],
  "connections": {
    "Webhook": {
      "main": [
        [
          {
            "node": "Données normalisées",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Données normalisées": {
      "main": [
        [
          {
            "node": "Infos officielles du plan (PDF)",
            "type": "main",
            "index": 0
          },
          {
            "node": "IA #2 – Vision Parser",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
