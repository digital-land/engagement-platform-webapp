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

		this.changeViewingEntity(0)
	}

	changeViewingEntity = (deltaIndex) => {
		let newIndex = this.currentEntityIndex + deltaIndex
		if (newIndex >= this.entities.length) {
			newIndex = 0
		}
		if (newIndex < 0) {
			newIndex = this.entities.length - 1
		}
		this.currentEntityIndex = newIndex
		const entity = this.entities[newIndex]
		this.changeDetails(entity)
		this.map.changeView(entity)
	}

	changeDetails = (entity) => {
		this.htmlElements.entityName.innerHTML = `${entity.attributes.Reference} - ${entity.attributes.Name}`
		let attributes = ''
		Object.entries(entity.attributes).forEach(([key, value]) => {
			attributes += `<div class='attribute ${key.replace(' ', '_')}'>${key}: ${value}</div>`
		})

		this.htmlElements.entityAttributes.innerHTML = attributes

		if (entity.errors) {
			let errors = ''
			Object.entries(entity.errors).forEach(([key, value]) => {
				errors += `<div class='errors ${key.replace(' ', '_')}'>${key}: ${value}</div>`
			})

			this.htmlElements.entityErrors.innerHTML = errors
		}
	}
}
