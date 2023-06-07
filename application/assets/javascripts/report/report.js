class ReportPage {
	constructor(entities) {
		this.currentEntityIndex = 0
		this.entities = entities
		this.htmlElements = {}

		this.map = new Map()
		this.map.addEntities(this.entities)

		this.htmlElements.nextButton = document.getElementById('nextButton')
		this.htmlElements.previousButton = document.getElementById('previousButton')
		this.htmlElements.entityName = document.getElementById('entityName')
		this.htmlElements.entityAttributes = document.getElementById('entityAttributes')
		this.htmlElements.entityErrors = document.getElementById('entityErrors')
		this.htmlElements.errorsList = document.getElementById('errorListBody')

		// this.changeViewingEntity(0)
		this.addErrorsToPage()
		this.centerMap()
	}

	addErrorsToPage = () => {
		this.entities.forEach((entity) => {
			entity.attributes.errors.forEach((error) => {
				this.addErrorToErrorsList(error, entity)
			})
		})
	}

	addErrorToErrorsList = (error, entity) => {
		const tr = document.createElement('tr')
		tr.className = 'errorRow'
		tr.onclick = () => {
			this.map.changeView(entity)
		}
		tr.innerHTML = `
			<td>${entity.attributes.Reference}</td>
			<td>${error.errorMessage}</td>
			<td>${error.columnNames}</td>
		    <td><a href='errors/${error.errorCode}'>More Info</a></td>
		`

		this.htmlElements.errorsList.appendChild(tr)
	}

	centerMap = () => {
		let bounds = [[-180, -90], [180, 90]]

		this.entities.forEach((entity) => {
			bounds = [
				[
					Math.max(bounds[0][0], entity.mapData.bounds[0][0]),
					Math.max(bounds[0][1], entity.mapData.bounds[0][1]),
				],
				[
					Math.min(bounds[1][0], entity.mapData.bounds[1][0]),
					Math.min(bounds[1][1], entity.mapData.bounds[1][1]),
				],
			]
		})

		this.map.map.fitBounds(bounds)
	}
}
