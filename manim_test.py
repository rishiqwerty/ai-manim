from manim import *

class HTTPServerScene(Scene):
    def construct(self):
        # Title
        title = Text("How an HTTP Server Works").scale(0.7)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Client (browser)
        client = Rectangle(width=3, height=1.5, color=BLUE).shift(LEFT * 4)
        client_label = Text("Client (Browser)", font_size=28).move_to(client.get_center())
        self.play(FadeIn(client), Write(client_label))

        # Server
        server = Rectangle(width=3, height=1.5, color=GREEN).shift(RIGHT * 4)
        server_label = Text("HTTP Server", font_size=28).move_to(server.get_center())
        self.play(FadeIn(server), Write(server_label))

        self.wait(1)

        # Request Arrow and Label
        request_arrow = Arrow(start=client.get_right(), end=server.get_left(), buff=0.2, color=YELLOW)
        request_label = Text("HTTP Request", font_size=24).next_to(request_arrow, UP)
        self.play(GrowArrow(request_arrow), Write(request_label))
        self.wait(1)

        # Server Processing Text
        processing = Text("Processing...", font_size=24, color=GREEN).next_to(server, DOWN)
        self.play(Write(processing))
        self.wait(1)
        self.play(FadeOut(processing))

        # Response Arrow and Label
        response_arrow = Arrow(start=server.get_left(), end=client.get_right(), buff=0.2, color=ORANGE)
        response_label = Text("HTTP Response", font_size=24).next_to(response_arrow, DOWN)
        self.play(GrowArrow(response_arrow), Write(response_label))
        self.wait(1)

        # Display Page on Client
        page_content = Text("Hello, World!", font_size=28, color=WHITE).next_to(client, DOWN)
        self.play(Write(page_content))
        self.wait(2)

        # Fade out everything
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        self.wait(1)
