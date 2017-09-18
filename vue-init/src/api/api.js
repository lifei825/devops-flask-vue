import axios from 'axios'
import Qs from 'qs'

export const baseUrl = 'http://127.0.0.1:8082';
// export const baseUrl = '';

export const getUserInfo = (username) => {
  return axios({
    method: 'GET',
    url: baseUrl + '/api/v1/user/' + username
  });
};

export const userLogin = (email, password) => {
  return axios({
    method: 'post',
    url: baseUrl + '/api/v1/login',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data: Qs.stringify({
      "email": email,
      "password": password
    })
  });
};

export const checkToken = (token) => {
  return axios({
    method: 'PUT',
    url: baseUrl + '/api/v1/login',
    headers: {
      'Authorization': 'JWT '+token
    }
  })
};



export default {
  getUserInfo,
  userLogin,
  checkToken
}
