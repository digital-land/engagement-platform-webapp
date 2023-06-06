/* global L */

class Map {
	baseStyle = {
		weight: 5,
		color: '#8286ed',
		pane: 'mapPane',
	}

	constructor() {
		this.map = L.map('map-1', {
			attributionControl: false,
			zoomControl: false,
			dragging: true,
			scrollWheelZoom: 'center',
		})

		L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
			maxZoom: 19,
			attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
		}).addTo(this.map)

		this.entities = []
		this.currentIndex = 0
	}

	addEntities = (entities) => {
		entities.map((entity) => {
			const newEntity = { ...entity }
			try {
				const polygon = L.geoJSON(
					{
						type: 'Polygon',
						coordinates: JSON.parse(newEntity.attributes.Geometry),
					},
				).addTo(this.map)
				newEntity.mapData.polygon = polygon
			} catch (e) {
				console.log(e)
			}
			return newEntity
		})
		this.entities = entities
	}

	changeView = (entity) => {
		// if (entities[newIndex].geometry.outsideUK) {
		// 	const point = JSON.parse(entities[newIndex].geometry.point)
		// 	const [, bounds] = calculateCentreAndBounds(
		// 		[
		// 			point[1],
		// 			point[0],
		// 		],
		// 		[
		// 			52,
		// 			-2,
		// 		],
		// 	)
		// 	console.log(`fitting bounds to mid point of line ${newIndex}`)
		// 	map.fitBounds(JSON.parse(bounds), { animate: true, duration: 0.5 })
		// }
		// else {
		console.log(`fitting bounds to ${entity.attributes.Name} (${entity.mapData.bounds})`)
		if (!entity.mapData.bounds) {
			this.map.fitWorld()
		} else {
			this.map.fitBounds(entity.mapData.bounds, { animate: true, duration: 0.5 })
		}
		// }
		this.resetAllHighlights()
		this.highlightGeometry(entity)
	}

	resetAllHighlights = () => {
		this.entities.forEach((entity) => {
			if (!entity.mapData.polygon) return
			entity.mapData.polygon.setStyle(this.baseStyle)
		})
	}

	highlightGeometry = (entity) => {
		try {
			this.map.removeLayer(entity.mapData.polygon)
			const polygon = L.geoJSON(
				{
					type: 'Polygon',
					coordinates: JSON.parse(entity.attributes.Geometry),
				},
			).setStyle({
				...this.baseStyle,
				color: '#FF0000',
				pane: 'overlayPane',
			}).addTo(this.map)

			entity.mapData.polygon = polygon
		} catch (e) {
			console.log(e)
		}
	}
}
