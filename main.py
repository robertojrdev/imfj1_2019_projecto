import cProfile

from application import Application as app

# Define a main function, just to keep things nice and tidy
def main():

    # Init application instance with main scene
    app.init("main", 800, 600)

    #Run application
    # cProfile.run("app.run()")
    app.run()
    return


# Run the main function
main()
