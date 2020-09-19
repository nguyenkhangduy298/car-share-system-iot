from matplotlib import pyplot as plt

class Plot:

    @staticmethod
    def plot_line_chart(x, y, title):
        plt.plot(x, y)
        plt.title(title)
        plt.savefig('images/Daily_active_user.png')
        plt.show()

    @staticmethod
    def plot_bar_chart(x, y, title):
        plt.bar(x, y)
        plt.title(title)
        plt.savefig('images/Bookings_by_cars.png')
        plt.show()

    @staticmethod
    def plot_pie_chart(x, y, title):
        plt.pie(y, labels=x, radius=1, autopct='%0.2f%%', 
            explode=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
        plt.title(title)
        plt.savefig('images/Monthly_bookings.png')
        plt.show()