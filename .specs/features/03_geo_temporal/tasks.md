# Tasks — Feature 03 (Geo-Temporal)

## T015: Geocoding municípios AL

- [ ] Baixar CSV de municípios AL do IBGE (ou geojson via `geobr`)
- [ ] Colunas mínimas: `codigo_ibge`, `nome`, `latitude`, `longitude`
- [ ] Salvar em `data/geo/municipios_al.csv` e `data/geo/municipios_al.geojson`
- [ ] Validar merge com `df['CIDADE DO FATO']` (tratar "Maceió" vs "Maceio" etc.)

## T016: Geocoding bairros top 5

- [ ] Para cada uma das 5 cidades, baixar polígonos de bairros (Nominatim batch ou shapefile IBGE)
- [ ] Fallback: centroide manual se OSM falhar
- [ ] Salvar em `data/geo/bairros_top5.csv`
- [ ] Validar cobertura ≥80% dos bairros nas 5 cidades

## T017: Choropleth + agregações

- [ ] Agregar contagem CVLI por (municipio, ano, mes) → CSV
- [ ] Plotar choropleth estático por município (Folium + screenshot ou matplotlib)
- [ ] Plotar evolução temporal: 4 subplots com janelas (1 ano, 3 anos, 5 anos, total)
- [ ] Tudo inline no notebook

## T018: HeatMap + série temporal

- [ ] Para cada cidade top 5, agregar (bairro, mes)
- [ ] Plotar HeatMap bairro (Folium)
- [ ] Série temporal: CVLI/dia agregado AL
- [ ] Heatmap dia_semana × hora (já gerado no NB01 — referenciar)
- [ ] Tudo inline

## Critérios de Aceitação

- Notebook roda end-to-end sem erro
- Pelo menos 4 visualizações espaciais diferentes
- CSVs gerados para o Streamlit consumir
