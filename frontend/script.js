const messagesEl = document.getElementById('messages')
const inputEl = document.getElementById('input')
const sendBtn = document.getElementById('send')

function addBubble(text, role='assistant'){
  const el = document.createElement('div')
  el.className = `bubble ${role}`
  el.textContent = text
  messagesEl.appendChild(el)
  messagesEl.scrollTop = messagesEl.scrollHeight
  return el
}
function addTyping(){
  const wrap = document.createElement('div')
  wrap.className='typing'
  wrap.innerHTML = '<div class=\"dot\"></div><div class=\"dot\"></div><div class=\"dot\"></div>'
  messagesEl.appendChild(wrap)
  messagesEl.scrollTop = messagesEl.scrollHeight
  return wrap
}

async function send(){
  const text = inputEl.value.trim()
  if(!text) return
  inputEl.value=''
  sendBtn.disabled = true
  addBubble(text,'user')
  const typing = addTyping()
  let assistantBubble = null
  let buffer = ''

  try{
    const resp = await fetch('http://127.0.0.1:8000/api/chat/stream', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ message: text })
    })
    const reader = resp.body.getReader()
    const decoder = new TextDecoder()
    while(true){
      const {done,value} = await reader.read()
      if(done) break
      const chunk = decoder.decode(value)
      for(const line of chunk.split('\\n')){
        if(line.startsWith('data: ')){
          const payload = line.slice(6)
          if(payload === '[DONE]') continue
          try{
            const data = JSON.parse(payload)
            if(data.meta){
              const meta = document.createElement('div')
              meta.className='meta'
              meta.textContent = `模型: ${data.meta.model} | 来源: ${data.meta.source}`
              messagesEl.appendChild(meta)
            }else if(data.content){
              buffer += data.content
              if(!assistantBubble){
                assistantBubble = addBubble('', 'assistant')
              }
              assistantBubble.textContent = buffer
            }
          }catch(e){}
        }
      }
    }
  }catch(err){
    addBubble('出现错误，请稍后重试。','assistant')
  }finally{
    typing.remove()
    sendBtn.disabled = false
  }
}

sendBtn.addEventListener('click', send)
inputEl.addEventListener('keydown', (e)=>{
  if(e.key==='Enter' && !e.shiftKey){
    e.preventDefault()
    send()
  }
})
