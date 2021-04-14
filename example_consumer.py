from pymercure.consumer import Consumer


def callback(message):
    print(f'Received message: {message.data}')

# token = '! CHANGE ME !'

c = Consumer(
    'https://localhost:3000/.well-known/mercure',
    ['test'],
    callback,
    verify=False,
    # headers={'Authorization': b'Bearer ' + token.encode()},
)
c.start_consumption()
