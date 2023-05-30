/* global L */

const entities = []

const calculateCentreAndBounds = (p1, p2) => {
	const x = (parseInt(p1[0], 10) + parseInt(p2[0], 10)) / 2
	const y = (parseInt(p1[1], 10) + parseInt(p2[1], 10)) / 2

	const bounds = `[[${p1}], [${p2}]]`

	return [`[${x},${y}]`, bounds]
}

let map

const changeDetails = (index) => {
	document.getElementById('entityName').innerHTML = `${entities[index].attributes.Reference} - ${entities[index].attributes.Name}`
	let attributes = ''
	Object.entries(entities[index].attributes).forEach(([key, value]) => {
		attributes += `<div class='attribute ${key.replace(' ', '_')}'>${key}: ${value}</div>`
	})

	document.getElementById('entityAttributes').innerHTML = attributes

	let errors = ''
	Object.entries(entities[index].errors).forEach(([key, value]) => {
		errors += `<div class='errors ${key.replace(' ', '_')}'>${key}: ${value}</div>`
	})

	document.getElementById('entityErrors').innerHTML = errors
}

const baseStyle = {
	weight: 5,
	color: '#8286ed',
	pane: 'mapPane',
}

const resetAllHighlights = () => {
	entities.forEach((entity) => {
		entity.geometry.polygon.setStyle(baseStyle)
	})
}

const highlightGeometry = (index) => {
	map.removeLayer(entities[index].geometry.polygon)

	console.log('adding')

	const polygon = L.geoJSON(
		{
			type: 'Polygon',
			coordinates: JSON.parse(entities[index].geometry.area),
		},
	).setStyle({
		...baseStyle,
		color: '#FF0000',
		pane: 'overlayPane',
	}).addTo(map)

	entities[index].geometry.polygon = polygon
}

/* eslint-disable no-unused-vars */
const geometry = (area, point, bounds, outsideUK) => ({
	area,
	point,
	bounds,
	outsideUK,
})

let currentIndex = 0

const changeView = (deltaIndex) => {
	let newIndex = currentIndex + deltaIndex
	if (newIndex >= entities.length) {
		newIndex = 0
	}
	if (newIndex < 0) {
		newIndex = entities.length - 1
	}
	if (entities[newIndex].geometry.outsideUK) {
		const point = JSON.parse(entities[newIndex].geometry.point)
		const [, bounds] = calculateCentreAndBounds(
			[
				point[1],
				point[0],
			],
			[
				52,
				-2,
			],
		)
		console.log(`fitting bounds to mid point of line ${newIndex}`)
		map.fitBounds(JSON.parse(bounds), { animate: true, duration: 0.5 })
	} else {
		console.log(`fitting bounds to ${newIndex}`)
		map.fitBounds(JSON.parse(entities[newIndex].geometry.bounds), { animate: true, duration: 0.5 })
	}
	currentIndex = newIndex
	resetAllHighlights()
	highlightGeometry(newIndex)
	changeDetails(newIndex)
}

/* eslint-disable no-unused-vars */
const initMap = () => {
	map = L.map('map-1', {
		attributionControl: false,
		zoomControl: false,
		dragging: true,
		scrollWheelZoom: 'center',
	})

	L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
		maxZoom: 19,
		attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
	}).addTo(map)

	entities.map((entity) => {
		const newEntity = { ...entity }
		const polygon = L.geoJSON(
			{
				type: 'Polygon',
				coordinates: JSON.parse(newEntity.geometry.area),
			},
		).addTo(map)
		newEntity.geometry.polygon = polygon
		return newEntity
	})

	changeView(0)
}
