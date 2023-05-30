const entities = [];

const calculateCentreAndBounds = (point1, point2) => {
    let x = (parseInt(point1[0]) + parseInt(point2[0])) / 2
    let y = (parseInt(point1[1]) + parseInt(point2[1])) / 2

    let bounds = `[[${point1}], [${point2}]]`

    return [`[${x},${y}]`, bounds]
}

let map;

const initMap = () => {
    map = L.map('map-1', {
        attributionControl: false,
        zoomControl: false,
        dragging: true,
        scrollWheelZoom: 'center'
    })

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    for(entity of entities){
        var polygon = L.geoJSON(
            {
                "type": "Polygon",
                "coordinates": JSON.parse(entity.geometry.area)
            }).addTo(map);
        entity.geometry.polygon = polygon
    }

    changeView(currentIndex)
}

let currentIndex = 0;

const changeView = (index) => {
    console.log(':: ' + index)
    if(index >= entities.length){
        index = 0
    }
    if(index < 0){
        index = entities.length - 1
    }
    console.log('fitting bounds to ' + index)
    map.fitBounds(JSON.parse(entities[index].geometry.bounds), {animate: true, duration: 0.5})
    currentIndex = index;
    resetAllHighlights()
    highlightGeometry(index)
    changeDetails(index)
}

const changeDetails = (index) => {
    document.getElementById('entityName').innerHTML = `${entities[index].attributes['Reference']} - ${entities[index].attributes['Name']}`
    attributes = '';
    for(const[key,value] of Object.entries(entities[index].attributes)){
        attributes += `<div class='attribute ${key.replace(' ', '_')}'>${key}: ${value}</div>`
    }

    document.getElementById('entityAttributes').innerHTML = attributes;

    errors = '';
    for(const[key,value] of Object.entries(entities[index].errors)){
        errors += `<div>${key}: ${JSON.stringify(value)}</div>`
    }

    document.getElementById('entityErrors').innerHTML = errors;
}

baseStyle = {
    weight: 5,
    color: '#8286ed',
    pane: 'mapPane'
}

const resetAllHighlights = () => {
    entities.forEach((entity) => {
        entity.geometry.polygon.setStyle(baseStyle)
    })
}

const highlightGeometry = (index) => {
    map.removeLayer(entities[index].geometry.polygon)

    console.log('adding')

    var polygon = L.geoJSON(
        {
            "type": "Polygon",
            "coordinates": JSON.parse(entities[index].geometry.area)
        }).setStyle({
            ...baseStyle,
            color: '#FF0000',
            pane: 'overlayPane'
        }).addTo(map);

    entities[index].geometry.polygon = polygon
}

const geometry = (area, point, bounds, outsideUK) => {
    return {
        area,
        point,
        bounds,
        outsideUK,
    }
}