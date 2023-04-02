import React, { useState } from 'react'
import "./PopupChat.css";
import ApiService from "../services/api";

import chatIcon from "../assets/chatIcon.png";

export const PopChat = ( props ) => {
  const [jawab, setJawab] = useState('');
  const [qt, setQt] = useState('');
  let hide = {
    display: 'none',
  }
  let show = {
    display: 'block'
  }
  let textRef = React.createRef()
  const {messages} = props

  const [chatopen, setChatopen] = useState(false)
  const toggle = e => {
    setChatopen(!chatopen)
  }

const handleSend = e => {
  // const qt1 = props.getMessage
  // qt1(textRef.current.value)
  console.log('hello')
  ApiService.post("http://localhost:8000/api/get_query", {
    question: qt,
  }).then((res) => {
        console.log(res);
        setJawab(res);
      })
    console.log('bye');
}

  return (
    <div id='chatCon'>
      <div class="chat-box" style={chatopen ? show : hide}>
    <div class="header">Chat with me</div>
    <div class="msg-area">
      {/* {
        messages.map((msg, i) => (
          i%2 ? (
          <p class="right"><span>{ msg }</span></p>
          ) : (
            <p class="left"><span>{ msg }</span></p>
          )
        ))
      } */}
    </div>
    <div class="footer">
      <input type="text" onChange={(e) => setQt(e.target.value)} ref={textRef} />
      <button onClick={handleSend}><i class="fa fa-paper-plane"></i></button>
    </div>
  </div>
    <div class="pop">
      <p><img onClick={toggle} src={chatIcon} alt="" /></p>
    </div>
    </div>
  )
}

export default PopChat