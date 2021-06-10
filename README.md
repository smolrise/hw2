Я экспериментировал с созданием собственных чартов, чтобы понять всю их подноготную, поэтому попытался максимально сделать на них.
Для запуска необходимо выполнить в дирректории hw2: helm install database ./users-db-chart/

После разматывания Postgres надо накатить на него Job:
kubectl apply -f initdb.yaml

Далее необходимо запустить само приложение совместно со сборокой. Для этого надо запустить 
skaffold run
либо, как альтернатива:
helm install app ./users-ws-chart/

После всех этих операций должен получиться рабочий сервис, доступный по:
curl -H'Host: arch.homework' http://<ip_kubernates>:31610/db | jq
Если необходимо получать ответ от сервиса по имени хоста, тогда в конец /etc/hosts надо добавить запись <ip_kubernates> arch.homework где <ip_kubernates> - это ip Kubernates. В моем случае, его можно получить командой minikube ip

API я немного упростил и ручка у меня называется /users, а не /user, как в предложенном дефолтовом примере
Протестировать приложение можно также следующими запросами:
curl -X POST -H'Host: arch.homework' -H "Content-Type: application/json" http://192.168.99.101:31610/users --data "@add_user.json"
curl -X PUT -H'Host: arch.homework' -H "Content-Type: application/json" http://192.168.99.101:31610/users/3 --data "@put_user.json"
curl -X DELETE -H'Host: arch.homework' http://192.168.99.101:31610/users/3

все JSON я закинул в корневую директорию.
