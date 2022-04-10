from itemadapter import ItemAdapter


class EcommerceScraperPipeline:
    def process_item(self, item, spider):
        for k, v in item.items():
            if not v:
                item[k] = ''
                continue
            if k == 'Title':
                item[k] = v.strip()
            elif k == 'ImageURL':
                item[k] = "/ ".join(v)
            elif k == 'price':
                item[k] = "$".join(v)
            elif k == 'Description':
                item[k] = ", ".join([i.strip() for i in v if i.strip()])
        
        return item
