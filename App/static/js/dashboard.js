name_input = document.getElementById('name-input')
name_submit = document.getElementById('name-submit')
name_edit = document.getElementById('name-edit');
name_discard = document.getElementById('name-discard')
email_input = document.getElementById('email-input')
email_submit = document.getElementById('email-submit')
email_edit = document.getElementById('email-edit')
email_discard = document.getElementById('email-discard')

name_discard.addEventListener('click', () => {
    location.reload()
})

name_edit.addEventListener('click', () => {
    name_input.disabled = false
    name_submit.type = 'submit'
})

try{
    email_discard.addEventListener('click',() => {
        location.reload()
    })

    email_edit.addEventListener('click', () => {
        email_input.disabled = false
        email_submit.type = 'submit'
    })
} catch (e){
    console.log(e)
}