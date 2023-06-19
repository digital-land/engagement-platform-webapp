class Upload {
	constructor() {
		this.content.selectDataType = document.getElementById('selectDataType')
		this.content.linkYourData = document.getElementById('linkYourData')
		this.content.uploadAFile = document.getElementById('uploadAFile')

		this.content.linkYourData.style.display = 'none'
		this.content.uploadAFile.style.display = 'none'
	}

	showLinkYourData() {
		this.content.linkYourData.style.display = 'block'
	}

	showUploadAFile() {
		this.content.uploadAFile.style.display = 'block'
	}
}
