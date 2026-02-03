package net.pterodactylus.sone.web.pages

import net.pterodactylus.sone.data.*
import net.pterodactylus.sone.main.*
import net.pterodactylus.sone.utils.*
import net.pterodactylus.sone.web.*
import net.pterodactylus.sone.web.page.*
import net.pterodactylus.util.template.*
import javax.inject.*

/**
 * Page that allows logged-in users to switch to a different Sone profile.
 */
@MenuName("SwitchProfile")
@TemplatePath("/templates/switchProfile.html")
@ToadletPath("switchProfile.html")
class SwitchProfilePage @Inject constructor(webInterface: WebInterface, loaders: Loaders, templateRenderer: TemplateRenderer) :
		LoggedInPage("Page.SwitchProfile.Title", webInterface, loaders, templateRenderer) {

	override fun handleRequest(soneRequest: SoneRequest, currentSone: Sone, templateContext: TemplateContext) {
		if (soneRequest.isPOST) {
			val soneId = soneRequest.httpRequest.getPartAsStringFailsafe("sone-id", 43)
			soneRequest.core.getLocalSone(soneId)?.let { sone ->
				setCurrentSone(soneRequest.toadletContext, sone)
				redirectTo("index.html")
			}
		}
		templateContext["sones"] = soneRequest.core.localSones.sortedWith(niceNameComparator)
		templateContext["currentSoneId"] = currentSone.id
	}

	override fun isEnabled(soneRequest: SoneRequest): Boolean =
			if (soneRequest.core.preferences.requireFullAccess && !soneRequest.toadletContext.isAllowedFullAccess) {
				false
			} else
				getCurrentSone(soneRequest.toadletContext) != null && soneRequest.core.localSones.size > 1

}
