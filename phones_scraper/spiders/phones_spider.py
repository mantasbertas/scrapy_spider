import scrapy

class PhonesSpider(scrapy.Spider):
    name = 'phones'
    start_urls = ['https://www.productindetail.com/']

    # counter for limiting how many to scrape in the constructor
    def __init__(self, limit=None, *args, **kwargs):
        super(PhonesSpider, self).__init__(*args, **kwargs)
        self.limit = int(limit) if limit else None
        self.count = 0

    # get phone page URL from home page (only starting  from home page due to the task asking for it)
    def parse(self, response):
        all_phones_url = response.css('a.dropdown-item[href="/phones"]::attr(href)').get()
        if all_phones_url:
            yield scrapy.Request(response.urljoin(all_phones_url), callback=self.parse_phone_list)

    # parse phone grid for title, image_url and detail_url
    def parse_phone_list(self, response):
        for phone in response.css('div.col-md-6.col-lg-4.col-xl-3.col-xxl-2.mb-4'):
            if self.limit and self.count >= self.limit:
                return

            item = {
                'product_name': phone.css('strong::text').get(),
                'image_url': phone.css('img.img-fluid.mb-3.hoverZoomLink::attr(src)').get(),
            }
            phone_detail_url = phone.css('a.text-decoration-none::attr(href)').get()
            if phone_detail_url:
                yield scrapy.Request(response.urljoin(phone_detail_url), callback=self.parse_phone_details,
                                     meta={'item': item})
            self.count += 1

        # pagination handling
        next_page = response.css('a.page-link[aria-label="Next"]::attr(href)').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse_phone_list)

    def parse_phone_details(self, response):
        item = response.meta['item']
        # grab all the remaining data points
        title = response.css('h1.fs-2 > strong::text').get()
        if title:
            parts = title.split(' ', 1)
            item['brand'] = parts[0]
            item['model'] = parts[1] if len(parts) > 1 else None

        # operating system
        os_div = response.css('div.col-sm-6.col-lg-4.mb-4:contains("Operating System")')
        os_value = os_div.css('small:nth-child(3)::text').get()
        item['operating_system'] = os_value.strip() if os_value else None

        #front camera resolution
        front_cam_div = response.css('div.col-sm-6.col-lg-4.mb-4:contains("Front Camera")')
        front_cam = front_cam_div.css('small:nth-child(3)::text').get()
        item['front_cam'] = front_cam.strip() if front_cam else None

        # main camera  resolution
        main_camera_div = response.css('div.col-sm-6.col-lg-4.mb-4:contains("Main Camera")')
        main_cam = main_camera_div.css('small:nth-child(3)::text').get()
        item['main_cam'] = main_cam.strip() if main_cam else None

        # display size and resolution
        display_div = response.css('div.col-sm-6.col-lg-4.mb-4:contains("Display")')
        display_info = display_div.css('small:nth-child(3)::text').get()
        display_parts = display_info.split(", ")
        item['display_size'] = display_parts[0].strip() if display_parts else None
        item['display_resolution'] = display_parts[1].strip() if display_parts else None

        # display type and techonology
        display_type = response.css('th:contains("Display Type") + td > small::text').get()
        item['display_type'] = display_type.strip() if display_type else None

        display_tech = response.css('th:contains("Display Technology") + td > small::text').get()
        item['display_technology'] = display_tech.strip() if display_tech else None
        item['image_url'] = response.css('div.col-sm-3.col-lg-3.col-xl-3 img::attr(src)').get()

        yield item
