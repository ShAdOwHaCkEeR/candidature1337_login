from dependency_injector.wiring import Provide, inject
from auth import Container, AuthClient
from dotenv import load_dotenv

@inject
def start(client: AuthClient = Provide[Container.Client]):
    client.run()
    return client

if __name__ == "__main__":
    load_dotenv()

    container = Container()
    
    container.config.username.from_env('USER_NAME')
    container.config.password.from_env('PASSWORD')

    container.wire(modules=[__name__])

    client = start()

    print(f"\n -Login\n\t -user[email]: {client.username}\n\t -user[password]: {client.password}\n\t -param: {client.param}\n\t -token: {client.token}")
    print(f"\n -Status\n\t -LoggedIn?: {client.valid}\n\t -KaynCheckIn?: {client.chkin_available}")
