import folium
map_osm = folium.Map(location=[36.5, 127], zoom_start=7, titles='food_store')
map_osm.save('test1.html')