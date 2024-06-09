import React, { useState } from 'react';
import './Home.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const Home = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [imagePreviewUrl, setImagePreviewUrl] = useState(null);
    const [imageData, setImageData] = useState([]);
    const [loading, setLoading] = useState(false);
    const fileSelectedHandler = (event) => {
        const file = event.target.files[0];
        if (!file){
            setImagePreviewUrl();
            setSelectedFile(null);
            return;
        } 
        setImageData([]);
        setSelectedFile(file);
        const reader = new FileReader();
        reader.onloadend = () => {
            setImagePreviewUrl(reader.result);
        };
        reader.readAsDataURL(file);
    };
    const fileUploadHandler = () => {
        if (!selectedFile){
            return;
        }
        const formData = new FormData();
        formData.append('file', selectedFile);
        setLoading(true);
        fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (response.ok) {
                return response.json(); // Chuyển đổi response thành đối tượng JSON
            } else {
                throw new Error('Response was not OK');
            }
        })
        .then(data => {
            setLoading(false);
            // Xử lý dữ liệu trả về từ backend
           setImageData(data);
        })
        .catch(error => {
            // Xử lý lỗi nếu cần
            console.error('Error occurred:', error);
        });
    };
    console.log(imageData);
    return (
        <div className='container mt-3'>
            <div className="input-group mb-3">
                <input type="file" className="form-control" id="inputGroupFile02" onChange={fileSelectedHandler} />
                <button type='submit' className="input-group-text submit_hover" htmlFor="inputGroupFile02" onClick={fileUploadHandler}>Upload</button>
            </div>
            <div className='input_img'>
                {selectedFile ===null ?
                 (
                    <div style={{
                        height: '256px',
                        width: '256px',
                        border: '1px solid gray',
                        borderRadius: '2px',
                        textAlign: 'center',
                    }}>
                        Ảnh đầu vào
                    </div>
                 ): 
                 (
                    <img src={imagePreviewUrl} alt="Preview" />
                )}
            </div>
            <div className='container mt-3'>
          <div className='output_img'>
            {
                imageData.length === 0 ? (
                    [1,2,3].map((index) => (
                        <div key={index} style={{
                            height: '256px',
                            width: '256px',
                            border: '1px solid gray',
                            borderRadius: '2px',
                            textAlign: 'center',
                            }}>
                            {
                                loading ? (
                                    <img src='loading.gif' alt='loading'/>
                                ) : 'Ảnh đầu ra'
                            }
                        </div>
                    ))
                ) : 
                (
                    imageData.map((image, index) => (
                        <img key={index} src={"http://127.0.0.1:5000/image/"+image} alt={'output'} />
                    ))
                )
            }
          </div>
        </div>
        </div>
    );
};

export default Home;
