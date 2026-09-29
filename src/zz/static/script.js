document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('register_form');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const fullname = document.getElementById('fullname').value.trim();
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();
            const confirmPassword = document.getElementById('confirm_password').value.trim();
            
            // Если на форме регистрации есть поле баланса — берем его, иначе шлем 1000
            const balanceInput = document.getElementById('balance');
            const balance = balanceInput ? balanceInput.value.trim() : 1000;

            if (password !== confirmPassword) {
                alert('Пароли не совпадают!');
                return false;
            }

            fetch('/user_register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: fullname,
                    email: email,
                    password: password,
                    balance: balance // ПЕРЕДАЕМ НА СЕРВЕР
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.result) {
                    window.location.href = `/you_loser?name=${encodeURIComponent(fullname)}&email=${encodeURIComponent(email)}&pass=${encodeURIComponent(password)}&balance=${data.balance}`;
                } else {
                    alert('Ошибка при регистрации в БД');
                }
            })
            .catch(error => {
                alert('Ошибка запроса к серверу при регистрации');
            });
        });
    }

    const loginForm = document.getElementById('login_form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = document.getElementById('login_email').value.trim();
            const password = document.getElementById('login_password').value.trim();

            fetch('/user_login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Неверный логин или пароль');
                }
            })
            .then(data => {
                // Подставляем баланс из БД (data.balance), который прислал Flask
                window.location.href = `/you_loser?name=${encodeURIComponent(data.name)}&email=${encodeURIComponent(email)}&pass=${encodeURIComponent(password)}&balance=${data.balance}`;
            })
            .catch(error => {
                alert(error.message);
            });
        });
    }
});
