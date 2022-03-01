#!/bin/bash

#SHA512
# TODO fix wrong signatures/RSA key format
#example

#curl -d
#{"publishNewFactCheck":
#    {"URLToCheckHash":"faceBookLinkHash",
#    "fingerPrintPublicKey":"9823475983475",
#    "URLwithFactCheck":"correctivLink",
#    "timestamp":"2020-03-02T11:18:21.456Z",
#    "signatureOnURLToCheckHashFingerPrintURLwithfactCheckTimestamp":"982347923847"}}
#localhost:8080/postendpoint

#https://twitter.com/SHomburg/status/1463401978076307456
#https://correctiv.org/faktencheck/2021/12/06/polizisten-sichern-weihnachtsmarkt-foto-entstand-in-frankreich-nicht-in-deutschland/
#SHA512
#ID-Cleartext in Form: <website><fingerprint><checksite>

curl -d '{"publishNewFactCheck":{"URLToCheckHash":"e3804d37ef8ec2f5a80b0e88434107e12600a3e02f054b3f9a1d05afc6c8a7be01d35e7ca8fdb92c93df22fc14caea226b9b5bf17959bf90815d09cffcbbfcc7","fingerPrintPublicKey":"D4401BEB947CE6386212333C78B657E23F8DD134","URLwithFactCheck":"https://correctiv.org/faktencheck/2021/12/06/polizisten-sichern-weihnachtsmarkt-foto-entstand-in-frankreich-nicht-in-deutschland/","timestamp":"Fri, 17 Dec 2021 12:10:44 GMT","signatureOnURLToCheckHashFingerPrintURLwithfactCheckTimestamp":"iQIzBAEBCgAdFiEE1EAb65R85jhiEjM8eLZX4j+N0TQFAmHcEEcACgkQeLZX4j+N0TTbchAAxUwrl8+EuQMN2mFytb9iwTJqQdw4uPQIo0NT1PKOuKOkf4wLwOJ7xVmIFXSib6nhJu7nTQqSjJjIOBVGeYw8+C2aiyI1orSALzgQ7x1RVQZqw4cl75dPUlhw8gJLlubsREuClvt8SuEAnFPilbRmy4OuHTcPgTDZcx3bF/xsMzNQEiAnY8ZX5p2j+IkvtjGf6pNDA245P0IQxYOGTZil89paPHLRC8Oavijljj+Y23GFVlSAvWezemNlUURIMqCp0BcHfxfE4I6rvK2g0svaSqGdsde74RedR0r0wYV7bmL8QV7OlQv31BK6grvkeDdC4pg/DuzCgCivZDtKJcaO45vA9nZE6QrrHlNvuA0ao1mDOY603vLGyZgtSuEHJH6Wd2EgHn8mGDMG56OUK9gKGriTYxrWWKVZHO6tETiOJpkwymE0qpBP6FpSCNWwxOJcJD4gi3C1q/JYS3w5VSNc60+jub9h3jiMll2EUTJfTlx5a9pv3nkJBKWqIlH58x/SIiKzXjmhHOWXXDNsojCbKHWDSVkIE2z9m+uVTHeAH1iNpwPvEbNvzTh3/q9P94h/VCoSFwh+1GznEbNTMQuXWiwhKfjhHMMKhYRj/3YrhnNAAc7DEKAI2foAW+SaeOROF/nTf4BcdyITQqbxgW1NG0GpGIG3icB0KnWMqiXOTts==N6CG"}}' localhost:8080/postendpoint

#https://twitter.com/C_W_M_O/status/1464241776697520130
#https://correctiv.org/faktencheck/2021/12/01/angebliches-tucholsky-gedicht-ueber-impfungen-stammt-von-satire-autor/

curl -d '{"publishNewFactCheck":{"URLToCheckHash":"f94c0f202a5029159b9c93f6470af36cf21982b2f11ccba4ea6538cb612cf9d7b9ccb6448ca491e2bf853360890d1463a6ac75e9858677a4641e134a10e56a93","fingerPrintPublicKey":"D4401BEB947CE6386212333C78B657E23F8DD134","URLwithFactCheck":"https://correctiv.org/faktencheck/2021/12/01/angebliches-tucholsky-gedicht-ueber-impfungen-stammt-von-satire-autor/","timestamp":"Sat, 18 Dec 2021 13:10:44 GMT","signatureOnURLToCheckHashFingerPrintURLwithfactCheckTimestamp":"iQIzBAEBCgAdFiEE1EAb65R85jhiEjM8eLZX4j+N0TQFAmHcEjwACgkQeLZX4j+N0TRabhAA579EbhrW91sps8KGPrnbbf1vJCGO0oLrv6TUs8ed9pw8M0D2QKXbrRcr8IMOHD3Q0HDltqkGgAML+BzOaRJJwmlmOy9gwbmKGzmRA0FeS6kt4d8TcNqgyhK0NdxMYlX5MqLz+cCrccMYM79Z+Egr50hqxcUritqMu6ztCZh5xz9bNayoZ2fp4pgZEjVdm+AR84o60O/RXkq46TkMrXptwtuB4AXV+EoccBjLUc4aNX0vDeALr4PyEKnKmFQe78/NYnv6I6moWSeI/plm/C7vdK3Iqk2SfpaJUhAeRq29zPdiahWWzKh1ywSNTWK2J+uuOcHHnimRKfcz223pTQRIAmbhQLyna/rn3nYGtChKe3ghLrwulIgmkMcFOpNjB4kdAr/G1z+mqJvcJ52xRkuzXQ6KuxJf3p7Xt8YJYxsdU/3JdU06JgGnuiGVCJxoqwgf7CK2VozEwHBUqeu9ECH35yuoe3m+J9e+Y/ZaJ3XIjUviw33EGAcqUnZyb6g26OMLwIZ0LcZ9o6jkk1DNeWyF82wE5Ddty3DvK3AUR5JWH9PCLrbFpfTx0mSM3jmtZfuA/deFleSW+LlZRttJOaxslhLTZadhwU7ge5nmnzorbrNj4n3ZqHnx9A/t3iqa2UDc1DhNWrvQaFpvzP66kGCdf+kVjqv46rZDpD8MqOfxmyo==enGK"}}' localhost:8080/postendpoint

#https://free-people.online/ard-gibt-praktisch-zu-das-es-eine-fake-pandemie-ist/
#https://correctiv.org/faktencheck/2021/12/02/nein-dieses-ard-video-von-oktober-2020-zeigt-nicht-dass-die-pandemie-ein-fake-sei/

curl -d '{"publishNewFactCheck":{"URLToCheckHash":"46475a00cb8b5b6e2459bc03eee81263c6693d83542df387154008a24c6f649881627204a3d8dc1d0f6b1fc675e4658a51ffb2d7bdd02cf5726291b63df6c6ac","fingerPrintPublicKey":"D4401BEB947CE6386212333C78B657E23F8DD134","URLwithFactCheck":"https://correctiv.org/faktencheck/2021/12/02/nein-dieses-ard-video-von-oktober-2020-zeigt-nicht-dass-die-pandemie-ein-fake-sei/","timestamp":"Sat, 18 Dec 2021 13:10:44 GMT","signatureOnURLToCheckHashFingerPrintURLwithfactCheckTimestamp":"iQIzBAEBCgAdFiEE1EAb65R85jhiEjM8eLZX4j+N0TQFAmHcFgEACgkQeLZX4j+N0TRJKBAAr9xw0mz7vWAaGxprtlPgKXCuB8KuNmOPWnmieL76XnEZ5YX9GiYvXfczVfhIUj8+4gqprs/+ZytEuvRRjQRa9y7a1ESXQBcS7U9qobE93dCUj0jxpibwRWZhUmPLIR8LJrUdFsxJKthm+rYsF63zrltBVc9ttiHXfs/AMq0XEafCv7x+FOd+fRS6VTGaE1NpJ7S1543oEPOtBw88VRtvKKb/G8sCsAXflsN1TnpjN40GriakTiqSoORvUOIcVduboZdl3nlmO0khS2FOAx2zrFZIA+e963UMwFcUT4gkDw5a4Onx+E6jqFxFRc52KpKUQ/D0zr+jBkLDHkBHpZ2kCycl22bOXLzEcktu+tIjaDF8Nt3fX0Nxue6IrQEzPEgfufZCQmWbfqCUb0v1w1ZSsOOBVGAFRFNVxJzeH6Mr57828SX3jglLJ8kcfaQe/RKYXZioi0Rc0YIvMQemBKl8WgWqz643VmPzlIvdQIMOsY2gLSo+oq/qMstK/RBXsmI0eNtpPzJGQR7ozVuE2DpiOaRUVngfMZr81oWsId1UdVUFvRmxNdfXUiF+rvA2Hcin+Pk6mIw7544C8p5h7JnhanVeRQRTMR+op76kS4GDR0QRxZx3pQnm7K88PFICCmJ6iXUi1RrYUfQa9B8tb6WvDeqCFCpVWfRK0QxffdkC6Z4==gOpo"}}' localhost:8080/postendpoint

#https://report24.news/who-bestaetigt-offiziell-covid-impfung-ist-gefaehrlich-wie-keine-andere/
#https://correctiv.org/faktencheck/2021/11/30/irrefuehrende-behauptungen-ueber-gemeldete-nebenwirkungen-nach-covid-19-impfungen-in-der-vigibase-datenbank-der-who/

curl -d '{"publishNewFactCheck":{"URLToCheckHash":"92c634194c4c0c96fc366365cfb0e754a6a4aec4dd989919678c2d1c5709ff8e3678e6f3bf8da6489340215070c59d429f5aef293654158e54baee4764e489a8","fingerPrintPublicKey":"D4401BEB947CE6386212333C78B657E23F8DD134","URLwithFactCheck":"https://correctiv.org/faktencheck/2021/11/30/irrefuehrende-behauptungen-ueber-gemeldete-nebenwirkungen-nach-covid-19-impfungen-in-der-vigibase-datenbank-der-who/","timestamp":"Sun, 19 Dec 2021 15:10:44 GMT","signatureOnURLToCheckHashFingerPrintURLwithfactCheckTimestamp":"iQIzBAEBCgAdFiEE1EAb65R85jhiEjM8eLZX4j+N0TQFAmHcF9gACgkQeLZX4j+N0TTziw//VAqBJwmdVURBtHDvVMb0HKAIWstRwqmcNluYPPkePw/yaQ0cyYjkufI+sQ81WMIOJob8zBza0umrxp7VD5gYGhRbWfET6apl5/yAKId7cVoNTtvgQkQEfhFuvxQcwIeM75ulfb+yjUpZA2X3ALdcd9oyg0kISzmIXKl1qAjgmDgjevf7Ctwg0o7pM8N7kTacj3fPUMvLFJx+1xKJXAbTl/nNlxoCUiX8e5AaFq1Ask06lKHPsZXsOMKmFD+toAvcgHxADjSxty3IRfF99UHzf7B9dgyvfgFv8ZMaPDRkwlx2gf78ZWWlCIK9jnIDYVY1nS/vRl4CqVW/UV/2I0ixk0pzouhd0nNiemDUvfMB10vRhlsM1Vpewo4nnAImEuotiMqu8N0DIfuQBkZY22r1n/Ul7zYoOGsuIEE5ijlqgg+PN6n/fMU5zvEiYdReO1sKABbvZxHQ2etIS2EjU6K8Ld9IE6qcM/rC5EOxQvXRFLvfG2iwirt7cFbO0xcrzgRMzC6w8vklVw27fLYaU3hsMOkPeW+MxAEi4cBdnYRvEigw+d0Y1a8sIEWLorTatk6J3EJ+RM1ROaD+deUNuI3cj6GH0deS+LIVyLQp3r58fhZm6BHA283A9hiQpAxn2D5967DGDBMZuJQLxiOJRUZYM5gguLof36/N9oNU/+POCTc==Om2b"}}' localhost:8080/postendpoint

#https://www.facebook.com/groups/1809346625750467/posts/4826709200680846/
#https://correctiv.org/faktencheck/2021/12/03/oesterreich-dieses-formular-aus-einer-impfstrasse-in-hainburg-an-der-donau-ist-seit-dem-22-november-veraltet/

curl -d '{"publishNewFactCheck":{"URLToCheckHash":"1fcb9f9a75847985b81192b4f57dc93ed516b85746e5c8b94cfafd7a62ab4b84c0814980c68e2743bb3061c54f3ada401865aa5fb21d3cdee8e4fa7510e9290a","fingerPrintPublicKey":"D4401BEB947CE6386212333C78B657E23F8DD134","URLwithFactCheck":"https://correctiv.org/faktencheck/2021/12/03/oesterreich-dieses-formular-aus-einer-impfstrasse-in-hainburg-an-der-donau-ist-seit-dem-22-november-veraltet/","timestamp":"Mon, 20 Dec 2021 19:10:44 GMT","signatureOnURLToCheckHashFingerPrintURLwithfactCheckTimestamp":"iQIzBAEBCgAdFiEE1EAb65R85jhiEjM8eLZX4j+N0TQFAmHcGSsACgkQeLZX4j+N0TTlkxAA88VG6fCaBR/4u5tZODBmN8DVCLZenpyHtbWkAAVF1nDs7X6vbItAfOtFx4ooVCWVrTbLvP6XUENp+/HhxokEpk5SivYbpIlTEwBQrkBkgwqAm6/QuoKkVNmxuu3dWOfv1kx9+o72R7i2F2LAbc9UiBMV/oF5rhZNVlpiuZ3RHT5yr9OaIedw8Ig9UR5FjJ10d2sMU157mI4M699M1sGpTenohkmhak/k0QqzPD29eTvI+uJJ9xwdgCgQ2kfrah/fXZ7U9SctXdrHglqfi/kZgVyAeZd5v8XlG3csbxOxJCZDNVf1o86SE7/dUyXMrxyFJ7AeN6uR3vber94CfQVAFxv7b89osgLMvPE5rPUxkXiRxm8vDCVq+2BaXPWwODEyaHf3ZR2EkPPx8zS54QKDq7rZvxZ84POfRpjw6WPiGVWZE7R8FwV7RkOfxUduD4wav1uCZnle0Yr73yS3Cfhf/A0RzWBQfMFf5+Bbpc4iHO5UpLsEcumb65R9oB7lp3V6vYydtYuwoKy/ec2iBu1Ui/Ss3ZFoOIwt5LtpM9AOM2yk6pzOZIn5npSow3054kh7G/wGpANPH/z3dopTOlvvLVblOxTIf1OlrXkdA6G0/KHVGWZiCxFzBORCadNlvb/273fKFEBNnjrhSL48cP8oZoAnskCiDCqWIFIyuQOW9TI==Zm9m"}}' localhost:8080/postendpoint
