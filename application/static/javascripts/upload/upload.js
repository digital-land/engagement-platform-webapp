class Upload {
	constructor() {
		this.content = {}
		this.initializeUploadSection()
	}

	showUploadAFile() {
		this.content.uploadAFile.style.display = 'block'
	}

	showArcgisLink() {
		this.content.arcgisLink.style.display = 'block'
	}

	initializeUploadSection() {
		const thiss = this
		document.addEventListener('DOMContentLoaded', () => {
			thiss.content.uploadAFile = document.getElementById('uploadAFile')
			thiss.content.uploadAFile.style.display = 'none'
			thiss.content.arcgisLink = document.getElementById('arcgisLink')
			thiss.content.arcgisLink.style.display = 'none'

			const radioButtons = document.getElementsByName('dataset')

			for (let i = 0; i < radioButtons.length; i += 1) {
				radioButtons[i].addEventListener('change', () => {
					thiss.handleDatasetChange()
				})
			}
		})
	}

	handleDatasetChange() {
		const uploadFileRadio = document.getElementById('uploadFile')
		const arcgisRadio = document.getElementById('arcGis')
		const uploadAFileSection = this.content.uploadAFile
		const arcgisLinkSection = this.content.arcgisLink

		if (uploadFileRadio.checked) {
			this.showUploadAFile()
		} else {
			uploadAFileSection.style.display = 'none'
		}

		if (arcgisRadio.checked) {
			this.showArcgisLink()
		} else {
			arcgisLinkSection.style.display = 'none'
		}
	}
}

const upload = new Upload()
