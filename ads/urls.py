from django.urls import path
from .views import AdView, SearchAdView, ExchangeProposalGetPostView, ExchangeProposalDeletePutView, AdDeletePutView

urlpatterns = [
	path("ad/", AdView.as_view(), name="ad"),
	path("ad/<int:ad_id>", AdDeletePutView.as_view(), name="change_ad_view"),
	path("ad/search/", SearchAdView.as_view(), name="search_ad_view"),
	path("proposal/", ExchangeProposalGetPostView.as_view(), name="get_post_exchange_proposal_view"),
	path("proposal/<int:proposal_id>/", ExchangeProposalDeletePutView.as_view(), name="put_delete_exchange_proposal_view")
]