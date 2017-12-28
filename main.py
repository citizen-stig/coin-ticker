import sys
import asyncio
import urwid


from fetchers import get_coinbase_spot_price


class Dashboard(object):
    palette = (
        ('normal', 'default', 'default'),
        ('price_lower', 'dark red', 'default'),
        ('price_higher', 'dark green', 'default'),
        ('streak', 'black', 'dark red'),
        ('bg', 'black', 'dark blue'),
    )
    coins = ('BTC', 'LTC', 'ETH')
    output_currency = ('EUR', '€')

    def __init__(self, timer=3):
        self.timer = timer
        self.prices = {k: None for k in self.coins}
        self.view = self.setup_view()

    @staticmethod
    def keypress(key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def setup_section(self, coin_name, price_value):
        text_color = 'normal'
        prev_price = self.prices.get(coin_name)
        if price_value is not None:
            if prev_price and price_value > prev_price:
                text_color = 'price_higher'
            elif prev_price and price_value < prev_price:
                text_color = 'price_lower'
            self.prices[coin_name] = price_value
            price_formatted = '{:10.2f} {}'.format(
                price_value,
                self.output_currency[1],
            ).rjust(10)
        else:
            price_formatted = 'N/A'

        price_text = urwid.Text(
            [
                ' {0}:'.format(coin_name),
                (text_color, price_formatted),
            ]
        )
        return urwid.LineBox(urwid.Filler(price_text, valign='top', top=1))

    def setup_view(self):
        sections = []
        for coin in self.coins:
            value = get_coinbase_spot_price(coin, self.output_currency[0])
            sections.append(self.setup_section(coin, value))
        return urwid.Pile(sections)

    def main(self):
        self.setup_view()
        evl = urwid.AsyncioEventLoop(loop=asyncio.get_event_loop())
        loop = urwid.MainLoop(
            self.view,
            palette=self.palette,
            unhandled_input=self.keypress,
            event_loop=evl)
        loop.set_alarm_in(self.timer, self.refresh)
        loop.run()

    def refresh(self, loop=None, data=None):
        if loop:
            loop.widget = self.setup_view()
            loop.set_alarm_in(self.timer, self.refresh, user_data=data)


def main():
    dashboard = Dashboard()
    sys.exit(dashboard.main())


if __name__ == '__main__':
    main()
