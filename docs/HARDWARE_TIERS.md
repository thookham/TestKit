# Hardware Tiers

TestKit organizes hardware into **Tiers** to help users select the right level of device popularity and support for their testing needs.

## Tier 1: Flagship & Global Standards

**"The Devices Everyone Uses"**

These are the most common enterprise and consumer devices found in millions of offices and homes. If your software needs to run anywhere, it must run on these.

* **Manufacturers**: Dell, HP, Lenovo, Apple, Microsoft.
* **Examples**: ThinkPad T-Series, Dell XPS, HP EliteBook, Surface Pro.
* **Availability**: Global.
* **Usage**: Primary development and testing targets.

## Tier 2: Enthusiast & Gaming

**"High Performance & Specific Use Cases"**

Devices with specialized hardware, typically discrete GPUs, high refresh rate screens, or unique form factors.

* **Manufacturers**: Razer, MSI, ASUS (ROG), Acer (Predator), Alienware.
* **Examples**: Razer Blade, ASUS Zephyrus, Steam Deck.
* **Usage**: Performance benchmarking, graphics testing, gaming optimization.

## Tier 3: Specialized & Rugged

**"The Edge Cases"**

Hardware designed for specific industries or environments. These often have unique constraints (low power, touch-only, ruggedized).

* **Manufacturers**: Panasonic (Toughbook), Zebra, Getac, Elo (POS).
* **Examples**: Panasonic Toughbook 33, Elo I-Series.
* **Usage**: Field service apps, Point of Sale (POS) software, military/industrial apps.

## Tier 4: Legacy & Niche (Beta)

**"The Long Tail"**

Older devices, regional exclusives, or experimental form factors.

* **Examples**:
  * **Legacy**: Windows XP/7 era laptops (Toshiba Satellite, Compaq).
  * **Niche**: Single Board Computers (SBCs) running Windows, Dual-screen prototypes.
  * **Regional**: Brands specific to Asia or Europe (e.g., Fujitsu Lifebook).
* **Usage**: Regression testing, ensuring backward compatibility.

---

## Choosing a Tier

| Goal | Recommended Tier |
|------|------------------|
| "I just need it to work for 90% of users" | **Tier 1** |
| "I'm building a 3D game" | **Tier 2** |
| "I'm building a kiosk app for a store" | **Tier 3** |
| "A client has a crash on an old laptop" | **Tier 4** |
