document.getElementById('sign-in').addEventListener('click', () => {
    document.getElementById('md-sign-in').classList.remove('hidden');
})

document.getElementById('close-md-sign-in').addEventListener('click', () => {
    document.getElementById('md-sign-in').classList.add('hidden');
})

document.getElementById('sign-up').addEventListener('click', () => {
    document.getElementById('md-sign-up').classList.remove('hidden');
})

document.getElementById('close-md-sign-up').addEventListener('click', () => {
    document.getElementById('md-sign-up').classList.add('hidden');
})

document.getElementById('sign-in-to-sign-up').addEventListener('click', () => {
    document.getElementById('md-sign-in').classList.add('hidden');
    document.getElementById('md-sign-up').classList.remove('hidden');
})

// ----------------------------------

// document.getElementById('#').addEventListener('click', () => {
//     document.querySelectorAll('.page-wrapper section').forEach(function(section) {
//         section.style.display = 'none';
//     });
//     document.querySelector('.info-contact').classList.add('hidden');
//     document.querySelector('.page-detail').classList.remove('hidden');
// })

// ---------------------Edit------------------

function EditInfo() {
    document.querySelector('#edit-avatar').classList.remove('hidden');
    document.querySelector('#edit-info').classList.remove('hidden');
    document.querySelectorAll('.edit-ac').forEach(function(element) {
        element.classList.remove('hidden');
    });    
    document.querySelector('#edit-avatar').classList.remove('hidden');
    document.querySelector('#edit-bio').classList.remove('hidden');

    document.querySelector('#div-edit').classList.add('hidden');
    document.querySelector('#div-save').classList.remove('hidden');
}

function Remove_ac(value) {
    if(value == 1) {
        document.querySelector('#a-fb').classList.add('hidden');
    } else if(value == 2) {
        document.querySelector('#a-lin').classList.add('hidden');
    } else {
        document.querySelector('#a-twi').classList.add('hidden');
    }
}

function Edit_Info_Agent() {
    var name = document.getElementById('info-name');
    var experience = document.getElementById('info-experience');
    var company = document.getElementById('info-company');
    var address = document.getElementById('info-address');
    var phone = document.getElementById('info-phone');

    name.style.display = 'none';
    experience.style.display = 'none';
    company.style.display = 'none';
    address.style.display = 'none';
    phone.style.display = 'none';

    var name_agent = document.getElementById('name-agent');
    var experience_agent = document.getElementById('experience-agent');
    var company_agent = document.getElementById('company-agent');
    var address_agent = document.getElementById('address-agent');
    var phone_number_agent = document.getElementById('phone-number-agent');

    name_agent.classList.remove('hidden');
    experience_agent.classList.remove('hidden');
    company_agent.classList.remove('hidden');
    address_agent.classList.remove('hidden');
    phone_number_agent.classList.remove('hidden');
}

function Edit_Info_Renter() {
    var name = document.getElementById('info-name');
    var address = document.getElementById('info-address');
    var phone = document.getElementById('info-phone');

    name.style.display = 'none';
    address.style.display = 'none';
    phone.style.display = 'none';

    var name_renter = document.getElementById('name-renter');
    var address_renter = document.getElementById('address-renter');
    var phone_number_renter = document.getElementById('phone-number-renter');

    name_renter.classList.remove('hidden');
    address_renter.classList.remove('hidden');
    phone_number_renter.classList.remove('hidden');
}

function Edit_Para() {
    var para_bio = document.getElementById('para-bio');
    var input_bio = document.getElementById('bio-agent');
    para_bio.style.display = 'none';
    input_bio.classList.remove('hidden');
}

function Edit_Para_Renter() {
    var para_bio = document.getElementById('para-bio');
    var input_bio = document.getElementById('bio-renter');
    para_bio.style.display = 'none';
    input_bio.classList.remove('hidden');
}

function previewImage(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            document.getElementById('img-avatar').src = e.target.result;
        }

        reader.readAsDataURL(input.files[0]);
    }
}