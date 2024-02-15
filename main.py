from RecipeServer import Server


def main():
    server = Server()
    server.run()


if __name__ == "__main__":
    main()
    # recipe = """
    #     STEP 1
    #     Generously season the steaks all over with salt, then press them down slightly with the palm of your hand so they’re roughly the same thickness. Heat the butter in a heavy-based frying pan over a medium-high heat until foaming, then add the thyme so it crackles and sizzles. Add the steaks and use tongs to turn them every 1 min over the course of 6 mins (for very rare), 8 mins (rare) or 10 mins (medium). This helps build an even crust on both sides. Remove the steaks to a warm plate and leave to rest while you make the sauce.
    #     STEP 2
    #     Scatter the pepper over the butter and thyme already in the pan. Toast for 1 min, then stir in the shallots and cook for another minute until they start to soften. Turn the heat up to high and tilt the pan so the side is against the flame (if using a gas hob). Carefully splash in the brandy. Flambé the shallots until the flames have died down.
    #     STEP 3
    #     Reduce the heat to medium and stir in the mustard and Worcestershire sauce. Bubble for a minute, then pour in the stock. Bring to the boil and cook for 2 mins until reduced by half. Stir in the crème fraîche and simmer until rich and creamy. Taste and add more salt if needed. Scoop out the thyme sprig, then return the steaks and any juices to the pan, spooning the sauce over the steaks. Sprinkle over the tarragon, if using. Bring the steaks to the table in the pan and serve drizzled with more sauce.
    # """  # noqa
    # processor = Processor()
    # res = processor.process(recipe)
    # print(json.dumps(res, indent=2, sort_keys=True))
