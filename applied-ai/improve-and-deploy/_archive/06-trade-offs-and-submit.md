---
title: "Trade-offs and Submit"
order: 6
---

You've deployed the same model two ways. They both work. The choice between them comes down to what you're actually trying to do.

> **With your partner:** Before reading the table below, talk through these questions.
>
> - Your model is 50MB and takes 2 seconds to run. Which deployment makes more sense?
> - Your model produces predictions that could be used to make medical decisions. Where would you want the data to stay?
> - You want to ship an update to the model without users having to do anything. Which approach makes that easier?

<details>
<summary>Reveal answer</summary>

There's no single right answer, but here's the reasoning:

A 50MB model that takes 2 seconds to run is probably a better fit for server-side inference. Downloading 50MB to every user's browser is slow, and running inference for 2 seconds on a low-end phone will be painful. A server can handle this once and return just the result.

Medical data is a strong argument for client-side inference. If patient images never leave the device, there's no server breach risk and fewer compliance concerns. Many privacy-sensitive applications are moving toward on-device inference for exactly this reason.

Model updates are easier on the server. You update the model file on your server and every user immediately gets the new version. With client-side inference, the model is cached in the browser. Forcing an update requires cache-busting.

</details>

## The trade-off summary

| | Server side | Browser side |
|---|---|---|
| **Where the model runs** | Your server | User's device |
| **Model stays private** | Yes | No, it's downloaded |
| **Works offline** | No | Yes, after first load |
| **Scales with users** | Server costs go up | Scales for free |
| **Model updates** | Instant | Requires cache-busting |
| **User data leaves device** | Yes | No |
| **Works on slow devices** | Yes | Depends on model size |

The right choice depends on your model size, your privacy requirements, your cost constraints, and how often you update the model.

## Submit

When you're done, share your notebook:

1. Click **Share** in the top right of Colab
2. Under "General access," change it to **"Anyone with the link"** and set the role to **Viewer**
3. Copy the link

**Both partners submit individually on Canvas** with the shared notebook link.

<div class="tally-embed-wrapper">
<iframe data-tally-src="https://tally.so/embed/ZjYqMa?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1&course=Applied+AI&unit=Improve+and+Deploy" loading="lazy" width="100%" height="539" frameborder="0" marginheight="0" marginwidth="0" title="Applied Course Feedback"></iframe>
</div>
<script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector('script[src="'+w+'"]')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s);}</script>
