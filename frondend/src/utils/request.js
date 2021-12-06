import axios from 'axios'

const service = axios.create({
  baseURL : "http://localhost:4999",
  timeout: 1000000
})

function postAction(url, parameter){
  return service({
    url: url,
    method: 'get',
    data: parameter
  })
}

export default postAction
