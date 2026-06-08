# Feature 03 — Geo-Temporal (NB03)

## Objetivo

Visualizar a evolução espaço-temporal dos CVLI em Alagoas:
- **Nível macro:** choropleth dos 102 municípios
- **Nível micro:** heatmap por bairro nas top 5 cidades
- **Janela temporal:** slider 2012-2026 + radio Mes/Trimestre/Semestre/Ano

## Geocoding (sem lat/lng na base original)

Base só tem `CIDADE DO FATO` (string) e `BAIRRO DO FATO` (string). Precisamos de coordenadas.

### Municípios
- Fonte: CSV IBGE (102 municípios AL)
- Atributo: `centroid_lat`, `centroid_lng` + geometria polígono (GeoJSON)

### Bairros (só top 5 cidades)
- Fonte: Nominatim OSM (offline cache) ou lookup manual centroides
- Top 5 por volume CVLI: Maceió, Arapiraca, Rio Largo, União dos Palmares, Marechal Deodoro

## Estrutura do NB03

```
// 1. Setup + paths
// 2. Carga base limpa + geo data
// 3. Geocoding municipios (merge IBGE)
// 4. Geocoding bairros top 5 (lookup ou Nominatim)
// 5. Agregacoes temporais
//    - municipio × mes
//    - municipio × trimestre
//    - municipio × semestre
//    - municipio × ano
//    - bairro × periodo (top 5)
// 6. Visualizacoes estaticas (PNG inline):
//    - Choropleth municipios
//    - HeatMap bairros Maceió
//    - HeatMap top 5
//    - Serie temporal CVLI/dia
//    - Heatmap dia_semana × hora
// 7. Exports para Streamlit (CSV agregado)
```

## Tasks (T015-T018)

| ID | Task | Estado |
|---|---|---|
| T015 | Geocoding municípios | ⏳ Pending |
| T016 | Geocoding bairros top 5 | ⏳ Pending |
| T017 | Choropleth + agregações temporais | ⏳ Pending |
| T018 | HeatMap bairro + serie temporal | ⏳ Pending |
