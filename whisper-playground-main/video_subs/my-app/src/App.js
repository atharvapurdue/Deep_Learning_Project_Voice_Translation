import axios from 'axios';
import React, { Component } from 'react';
import { saveAs } from 'file-saver';

class App extends Component {
	subfile = null
	state = {
		selectedFile: null
	};

	onFileChange = event => {
		this.setState({ selectedFile: event.target.files[0] });
	};

	onFileUpload = () => {

		const formData = new FormData();

		formData.append(
			"myFile",
			this.state.selectedFile,
			this.state.selectedFile.name
		);

		axios({
			url: 'http://localhost:8000/videosub', //your url
			method: 'POST',
			data: formData,
			headers: { "Content-Type": 'multipart/form-data' },
			responseType: 'blob', // important
		}).then((res) => {
			console.log(res.data)
			saveAs(res.data, "video.mp4");
		})
	};

	fileData = () => {

		if (this.state.selectedFile) {

			return (
				<div>
					<h2>File Details:</h2>
					<p>File Name: {this.state.selectedFile.name}</p>

					<p>File Type: {this.state.selectedFile.type}</p>

					<p>
						Last Modified:{" "}
						{this.state.selectedFile.lastModifiedDate.toDateString()}
					</p>
				</div>

			);
		} else {
			return (
				<div>
					<br />
					<h3 style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>Choose before Pressing the Upload button</h3>
				</div>
			);
		}
	};

	render() {
		return (

			<div style={{
				backgroundColor: '#873e23'
			}}>
				<h1 style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
					Add Subtitles To Your Videos!
				</h1>
				<div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
					<input type="file" onChange={this.onFileChange} />
					<button onClick={this.onFileUpload}>
						Upload!
					</button>
				</div>
				{this.fileData()}
			</div>
		);
	}
}
export default App;
